import requests

TARGET_HOST = "http://simon.benbilal237free.xyz:80"

def app(environ, start_response):
    url = TARGET_HOST + environ.get("PATH_INFO", "/")
    if environ.get("QUERY_STRING"):
        url += "?" + environ["QUERY_STRING"]

    method = environ["REQUEST_METHOD"]
    headers = {k[5:].replace("_", "-").title(): v for k, v in environ.items() if k.startswith("HTTP_")}
    headers["Host"] = "simon.benbilal237free.xyz"

    try:
        length = int(environ.get("CONTENT_LENGTH", 0))
    except (ValueError, TypeError):
        length = 0

    body = environ["wsgi.input"].read(length) if length > 0 else None

    try:
        resp = requests.request(method, url, headers=headers, data=body, stream=True, timeout=10)
        status = f"{resp.status_code} {resp.reason}"
        response_headers = [(k, v) for k, v in resp.headers.items() if k.lower() != "transfer-encoding"]
        start_response(status, response_headers)
        return resp.iter_content(chunk_size=4096)
    except Exception as e:
        start_response("400 Bad Request", [("Content-Type", "text/plain")])
        return [b"Bad Request"]
