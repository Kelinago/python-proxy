from flask import Flask, Response, request as flask_request
from urllib.parse import urljoin

import requests

from utils import filter_headers, encode_content, modify_response_html, modify_response_text


app = Flask('ProxyApp', static_url_path='/flask_static')


proxy_host: str = 'en.wikipedia.org'
BASE_URL = f'https://{proxy_host}/'


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def generic_proxy(path: str):
    request_headers = filter_headers(dict(flask_request.headers.items()))
    target_url = urljoin(BASE_URL, path)

    if 'referer' in request_headers:
        request_headers['referer'] = urljoin(BASE_URL, path)

    try:
        with requests.Session() as session:
            response = session.request(
                method=flask_request.method,
                url=target_url,
                headers=request_headers,
                params=flask_request.args.to_dict(),
                cookies=flask_request.cookies.to_dict(),
                json=flask_request.get_json(silent=True) or {},
                allow_redirects=True
            )
    except requests.RequestException:
        return Response(f"Unable to retrieve content from {target_url}", status=503)

    response_headers = filter_headers(response.headers)
    response_content_type = response_headers.get('content-type', '')
    content_encoding = response_headers.get('content-encoding', 'identity')

    response_body = response.content
    if 'text/html' in response_content_type:
        response_body = modify_response_html(response.text)
    elif 'text/plain' in response_content_type:
        response_body = modify_response_text(response.text)

    response_body = encode_content(response_body, content_encoding)

    return Response(
        response_body,
        response.status_code,
        response_headers
    )
