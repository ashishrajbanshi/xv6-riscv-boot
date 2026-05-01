import json
import os
from wsgiref.simple_server import make_server

from handler import handler as trigger_handler
from noop_handler import handler as noop_handler


def _status_line(status_code: int) -> str:
    if status_code == 200:
        return "200 OK"
    if status_code == 404:
        return "404 Not Found"
    if status_code == 405:
        return "405 Method Not Allowed"
    if status_code == 500:
        return "500 Internal Server Error"
    return f"{status_code} Unknown"


def app(environ, start_response):
    method = environ.get("REQUEST_METHOD", "GET").upper()
    path = environ.get("PATH_INFO", "/")

    if method not in {"GET", "POST"}:
        payload = {"statusCode": 405, "body": {"error": "method not allowed"}}
    elif path in {"/", "/trigger"}:
        payload = trigger_handler({}, None)
    elif path == "/noop":
        payload = noop_handler({}, None)
    elif path == "/healthz":
        payload = {"statusCode": 200, "body": {"status": "ok"}}
    else:
        payload = {"statusCode": 404, "body": {"error": "not found"}}

    status = _status_line(int(payload.get("statusCode", 200)))
    response_bytes = json.dumps(payload).encode("utf-8")
    headers = [
        ("Content-Type", "application/json"),
        ("Content-Length", str(len(response_bytes))),
    ]
    start_response(status, headers)
    return [response_bytes]


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    with make_server("0.0.0.0", port, app) as server:
        server.serve_forever()
