import json
from urllib.parse import urlparse, urlencode


# 构造 GET 请求
def build_get_request(uri, headers=None):
    path = uri.path or "/"
    if uri.query:
        path += f"?{uri.query}"

    request_line = f"GET {path} HTTP/1.1"
    default_headers = {
        "Host": uri.host,
        "User-Agent": "MyCustomBrowser/1.0",
        "Connection": "Keep-Alive"
    }

    if headers:
        default_headers.update(headers)

    headers_str = "\r\n".join(f"{key}: {value}" for key, value in default_headers.items())
    return f"{request_line}\r\n{headers_str}\r\n\r\n"


# 构造 HEAD 请求（同 GET，但无 Body）
def build_head_request(uri, headers=None):
    path = uri.path or "/"
    if uri.query:
        path += f"?{uri.query}"

    request_line = f"HEAD {path} HTTP/1.1"
    default_headers = {
        "Host": uri.host,
        "User-Agent": "MyCustomBrowser/1.0",
        "Connection": "Keep-Alive"
    }

    if headers:
        default_headers.update(headers)

    headers_str = "\r\n".join(f"{key}: {value}" for key, value in default_headers.items())
    return f"{request_line}\r\n{headers_str}\r\n\r\n"


# 构造 POST 请求
def build_post_request(uri, data, headers=None, content_type="application/json"):
    path = uri.path or "/"
    if uri.query:
        path += f"?{uri.query}"

    request_line = f"POST {path} HTTP/1.1"

    if content_type == "application/json":
        body = json.dumps(data)
    elif content_type == "application/x-www-form-urlencoded":
        body = urlencode(data)
    else:
        raise ValueError("Unsupported Content-Type")

    default_headers = {
        "Host": uri.host,
        "User-Agent": "MyCustomBrowser/1.0",
        "Content-Type": content_type,
        "Content-Length": str(len(body)),
        "Connection": "Keep-Alive"
    }

    if headers:
        default_headers.update(headers)

    headers_str = "\r\n".join(f"{key}: {value}" for key, value in default_headers.items())
    return f"{request_line}\r\n{headers_str}\r\n\r\n{body}"


# 注入默认请求头
def inject_default_headers(headers, host, keep_alive=True, user_agent=None):
    if headers is None:
        headers = {}

    headers.setdefault("Host", host)
    headers.setdefault("User-Agent", user_agent or "MyCustomBrowser/1.0")
    headers.setdefault("Connection", "Keep-Alive" if keep_alive else "Close")

    return headers
