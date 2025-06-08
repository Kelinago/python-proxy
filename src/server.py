from flask import Flask, jsonify, request

app = Flask(__name__)

METHOD_TO_CODE = {
    'GET': 200,
    'POST': 201,
    'PUT': 200,
    'DELETE': 204
}

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy(path):
    request_info = {
        "method": request.method,
        "path": path,
        "headers": dict(request.headers),
        "params": request.args.to_dict(),
        "cookies": request.cookies.to_dict(),
        "data": request.get_json(silent=True) or {}
    }

    return jsonify(request_info), METHOD_TO_CODE.get(request.method, 200)
