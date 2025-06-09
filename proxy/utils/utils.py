from io import BytesIO
from bs4 import BeautifulSoup
import gzip
import zlib
from proxy.handlers import WordLengthMarkerHandler


def encode_content(text, content_encoding, text_encoding='utf-8'):
    if isinstance(text, str):
        text = text.encode(text_encoding)
    if content_encoding == 'identity':
        data = text
    elif content_encoding in ('gzip', 'x-gzip'):
        io = BytesIO()
        with gzip.GzipFile(fileobj=io, mode='wb') as f:
            f.write(text)
        data = io.getvalue()
    elif content_encoding == 'deflate':
        data = zlib.compress(text)
    else:
        raise Exception("Unknown Content-Encoding: %s" % content_encoding)
    return data


def modify_response_html(text: str) -> str:
    modify_handler = WordLengthMarkerHandler()
    soup = BeautifulSoup(text, 'html.parser')

    if not soup.body:
        return text

    for node in soup.body.find_all(text=True):
        if not any((
            node.find_parent('script'),
            node.find_parent('link'),
        )):
            node.replace_with(modify_handler.handle(node.text))

    return str(soup)


def modify_response_text(text: str) -> str:
    modify_handler = WordLengthMarkerHandler()
    return modify_handler.handle(text)

_hop_by_hop_headers = (
    'connection',
    'keep-alive',
    'proxy-authenticate',
    'proxy-authorization',
    'te',
    'trailers',
    'transfer-encoding',
    'upgrade',
    'host',
)

def filter_headers(headers):
    return {
        k.lower(): v
        for k, v in headers.items()
        if k.lower() not in _hop_by_hop_headers
    }