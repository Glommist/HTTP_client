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
def build_post_request(uri, data, headers=None, file_path=None, content_type="application/json"):
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

    # 处理 JSON 数据
    if data and not file_path:
        body = json.dumps(data)
        default_headers["Content-Type"] = "application/json"
        default_headers["Content-Length"] = str(len(body))

    # 处理文件上传
    elif file_path:
        boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
        file_name = os.path.basename(file_path)
        mime_type = mimetypes.guess_type(file_name)[0] or "application/octet-stream"

        with open(file_path, "rb") as f:
            file_content = f.read()

        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="file"; filename="{file_name}"\r\n'
            f"Content-Type: {mime_type}\r\n\r\n"
        ).encode() + file_content + f"\r\n--{boundary}--\r\n".encode()

        default_headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"
        default_headers["Content-Length"] = str(len(body))

    else:
        raise ValueError("POST 请求需要提供 data 或 file_path")

    # 合并用户自定义 Headers
    if headers:
        default_headers.update(headers)

    headers_str = "\r\n".join(f"{key}: {value}" for key, value in default_headers.items())
    
    # 如果是 JSON，则返回字符串；如果是文件上传，则返回二进制数据
    if file_path:
        request = f"{request_line}\r\n{headers_str}\r\n\r\n".encode() + body
    else:
        request = f"{request_line}\r\n{headers_str}\r\n\r\n{body}"

    return request


# 注入默认请求头
def inject_default_headers(headers, host, keep_alive=True, user_agent=None):
    if headers is None:
        headers = {}

    headers.setdefault("Host", host)
    headers.setdefault("User-Agent", user_agent or "MyCustomBrowser/1.0")
    headers.setdefault("Connection", "Keep-Alive" if keep_alive else "Close")

    return headers

import mimetypes
import os
def build_multipart_form_data(file_path):
    """构造 multipart/form-data 格式的请求体"""
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    file_name = os.path.basename(file_path)
    mime_type = mimetypes.guess_type(file_name)[0] or "application/octet-stream"

    with open(file_path, "rb") as f:
        file_content = f.read()

    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{file_name}"\r\n'
        f"Content-Type: {mime_type}\r\n\r\n"
    ).encode() + file_content + f"\r\n--{boundary}--\r\n".encode()

    headers = {
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "Content-Length": str(len(body))
    }

    return body, headers
