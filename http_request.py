import socket
import ssl
import json
from urllib.parse import urlparse


def create_connection(uri):
    """根据 URL 创建 HTTP 或 HTTPS 连接"""
    scheme = uri.scheme
    host = uri.host
    port = uri.port or (443 if scheme == "https" else 80)

    sock = socket.create_connection((host, port))

    if scheme == "https":
        context = ssl.create_default_context()
        sock = context.wrap_socket(sock, server_hostname=host)

    return sock


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


def inject_default_headers(headers, host, keep_alive=True, user_agent=None):
    if headers is None:
        headers = {}

    headers.setdefault("Host", host)
    headers.setdefault("User-Agent", user_agent or "MyCustomBrowser/1.0")
    headers.setdefault("Connection", "Keep-Alive" if keep_alive else "Close")

    return headers


def send_request(uri, method="GET", headers=None, data=None):
    """通用的 HTTP 请求发送函数，支持 GET/HEAD/POST"""
    parsed_uri = urlparse(uri)
    sock = create_connection(parsed_uri)

    if method == "GET":
        request = build_get_request(parsed_uri, headers)
    elif method == "HEAD":
        request = build_head_request(parsed_uri, headers)
    elif method == "POST":
        request = build_post_request(parsed_uri, data, headers)
    else:
        raise ValueError("Unsupported HTTP method")

    sock.sendall(request.encode())

    response = sock.recv(4096).decode()
    sock.close()
    return response

