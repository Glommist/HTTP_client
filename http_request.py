import socket
import ssl
import json
from urllib.parse import urlparse


def create_connection(uri):
    """创建 HTTP/HTTPS 连接"""
    scheme = uri.scheme
    host = uri.hostname
    port = uri.port or (443 if scheme == "https" else 80)

    sock = socket.create_connection((host, port))

    if scheme == "https":
        context = ssl.create_default_context()
        sock = context.wrap_socket(sock, server_hostname=host)

    return sock


def build_request(method, uri, headers=None, body=None):
    """构建 HTTP 请求（支持 GET、HEAD、POST）"""
    path = uri.path or "/"
    host = uri.hostname
    port = uri.port or (443 if uri.scheme == "https" else 80)

    request_line = f"{method} {path} HTTP/1.1"
    default_headers = {
        "Host": host,
        "User-Agent": "MyCustomBrowser/1.0",
        "Connection": "Keep-Alive"
    }

    if headers:
        default_headers.update(headers)

    if body:
        body = json.dumps(body)
        default_headers["Content-Type"] = "application/json"
        default_headers["Content-Length"] = str(len(body))
    else:
        body = ""

    headers_str = "\r\n".join(f"{key}: {value}" for key, value in default_headers.items())
    return f"{request_line}\r\n{headers_str}\r\n\r\n{body}"


def send_request(uri, method="GET", headers=None, body=None):
    """发送 HTTP 请求并返回响应"""
    parsed_uri = urlparse(uri)
    sock = create_connection(parsed_uri)
    request = build_request(method, parsed_uri, headers, body)

    sock.sendall(request.encode())

    response = sock.recv(4096).decode()  # 读取服务器响应
    sock.close()
    return response


# 示例用法
url = "https://www.example.com"
print(send_request(url))  # 发送 GET 请求

url_post = "https://postman-echo.com/post"
print(send_request(url_post, "POST", body={"key": "value"}))  # 发送 POST 请求
