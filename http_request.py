import socket
import ssl
import json


# 构造 GET 请求
def build_get_request(uri, headers=None):
    path = uri.path or "/"
    host = uri.host
    port = uri.port or (443 if uri.scheme == "https" else 80)

    request_line = f"GET {path} HTTP/1.1"
    default_headers = {
        "Host": host,
        "User-Agent": "MyCustomBrowser/1.0",
        "Connection": "Keep-Alive"
    }

    if headers:
        default_headers.update(headers)

    headers_str = "\r\n".join(f"{key}: {value}" for key, value in default_headers.items())
    return f"{request_line}\r\n{headers_str}\r\n\r\n"

# 构造 HEAD 请求
def build_head_request(uri, headers=None):
    path = uri.path or "/"
    host = uri.host
    port = uri.port or (443 if uri.scheme == "https" else 80)

    request_line = f"HEAD {path} HTTP/1.1"
    default_headers = {
        "Host": host,
        "User-Agent": "MyCustomBrowser/1.0",
        "Connection": "Keep-Alive"
    }

    if headers:
        default_headers.update(headers)

    headers_str = "\r\n".join(f"{key}: {value}" for key, value in default_headers.items())
    return f"{request_line}\r\n{headers_str}\r\n\r\n"

# 构造 POST 请求
def build_post_request(uri, data, headers=None):
    path = uri.path or "/"
    host = uri.host
    port = uri.port or (443 if uri.scheme == "https" else 80)

    request_line = f"POST {path} HTTP/1.1"
    body = json.dumps(data)
    default_headers = {
        "Host": host,
        "User-Agent": "MyCustomBrowser/1.0",
        "Content-Type": "application/json",
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