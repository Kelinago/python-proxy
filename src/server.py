from flask import Flask, Response, request as flask_request
from urllib.parse import urljoin
import requests

from handlers import WordLengthMarkerHandler


app = Flask('ProxyApp')


proxy_host: str = 'en.wikipedia.org'
BASE_URL = f'https://{proxy_host}/'

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def generic_proxy(path: str):
    request_headers = dict(flask_request.headers.items())
    request_headers['Host'] = proxy_host

    with requests.Session() as session:
        response = session.request(
            method=flask_request.method,
            url=urljoin(BASE_URL, path),
            headers=request_headers,
            params=flask_request.args.to_dict(),
            cookies=flask_request.cookies.to_dict(),
            json=flask_request.get_json(silent=True) or {},
            allow_redirects=False
        )

    modified_text = WordLengthMarkerHandler().handle(response.text)

    return Response(
        modified_text,
        response.status_code,
        response.headers
    )
