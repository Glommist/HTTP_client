# 解析响应，处理重定向、chunked等
import socket


def read_response(sock) -> tuple:
    """
    解析 HTTP 响应，返回 (status_line, headers_dict, body_bytes)
    """
    # 读取响应头
    response_data = b""
    while b"\r\n\r\n" not in response_data:
        chunk = sock.recv(4096)
        if not chunk:
            break
        response_data += chunk

    # 分割 响应头 和 响应体
    header_part, _, body = response_data.partition(b"\r\n\r\n")

    # 解析状态行和头部
    lines = header_part.decode().split("\r\n")
    status_line = lines[0]  # HTTP/1.1 200 OK
    headers = {k: v for k, v in (line.split(": ", 1) for line in lines[1:])}

    # 解析状态码
    status_code = int(status_line.split()[1])

    # 处理 Chunked 传输
    if headers.get("Transfer-Encoding", "").lower() == "chunked":
        body = handle_chunked_body(body, sock)

    # 处理 Gzip 压缩
    if headers.get("Content-Encoding", "").lower() == "gzip":
        body = decompress_gzip(body)

    return status_line, headers, body


def handle_chunked_body(body_bytes, sock):
    """
    解析 Chunked 传输的响应体
    """
    body = b""
    while True:
        # 读取 chunk size
        chunk_size_str = b""
        while not chunk_size_str.endswith(b"\r\n"):
            chunk_size_str += sock.recv(1)

        chunk_size = int(chunk_size_str.strip(), 16)
        if chunk_size == 0:
            break  # 结束 Chunked 传输

        # 读取 chunk 数据
        chunk_data = b""
        while len(chunk_data) < chunk_size:
            chunk_data += sock.recv(chunk_size - len(chunk_data))

        # 读取 chunk 结尾的 `\r\n`
        sock.recv(2)

        body += chunk_data

    return body


import gzip
import io

def decompress_gzip(body_bytes):
    """
    解压 Gzip 编码的 HTTP 响应体
    """
    with gzip.GzipFile(fileobj=io.BytesIO(body_bytes)) as f:
        return f.read()

def is_redirect(status_code):
    """
    判断 HTTP 状态码是否是重定向
    """
    return status_code in (301, 302, 303, 307, 308)

def get_redirect_location(headers):
    """
    获取 `Location` 头部，返回重定向的 URL
    """
    return headers.get("Location")
