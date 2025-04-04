# 构造GET、HEAD、POST请求
from urllib.parse import urlparse

def build_get_request(uri, headers=None):
    path = uri.path or "/"  # 默认路径为 "/"
    host = uri.host
    port = uri.port or 80   # 默认 HTTP 端口 80

    request_line = f"GET {path} HTTP/1.1"
    default_headers = {
        "Host": host,
        "User-Agent": "MyCustomBrowser/1.0",
        "Connection": "Keep-Alive"
    }
    
    if headers:
        default_headers.update(headers)  # 合并用户传入的 headers

    # 组合 HTTP 头部
    headers_str = "\r\n".join(f"{key}: {value}" for key, value in default_headers.items())
    return f"{request_line}\r\n{headers_str}\r\n\r\n"


def build_head_request(uri, headers=None):
    path = uri.path or "/"
    host = uri.host
    port = uri.port or 80

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


import json

def build_post_request(uri, data, headers=None):
    path = uri.path or "/"
    host = uri.host
    port = uri.port or 80

    request_line = f"POST {path} HTTP/1.1"
    body = json.dumps(data)  # 发送 JSON 数据
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


def inject_default_headers(headers, host, keep_alive=True, user_agent=None):
    if headers is None:
        headers = {}

    headers.setdefault("Host", host)
    headers.setdefault("User-Agent", user_agent or "MyCustomBrowser/1.0")
    headers.setdefault("Connection", "Keep-Alive" if keep_alive else "Close")

    return headers
