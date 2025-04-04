# 解析响应，处理重定向、chunked等
import socket

import gzip

def read_line(sock):
    """从 socket 读取一行数据，直到 \r\n"""
    line = b""
    while not line.endswith(b"\r\n"):
        chunk = sock.recv(1)  # 一次读取 1 字节，确保逐行解析
        if not chunk:
            break
        line += chunk
    return line.strip().decode(errors='ignore')
def recv_exact(sock, size):
    """确保读取完整的 size 字节"""
    data = b""
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            break
        data += chunk
    return data

def handle_chunked_body(body, sock):
    decoded_body = b""
    while True:
        chunk_size_line = read_line(sock)
        try:
            chunk_size = int(chunk_size_line, 16)  # 16 进制解析 chunk 大小
        except ValueError:
            print(f"Skipping invalid chunk size: {repr(chunk_size_line)}")
            continue  # 跳过无效的 chunk size
        if chunk_size == 0:
            break  # 结束处理
        chunk_data = recv_exact(sock, chunk_size)
        sock.recv(2)  # 读取 \r\n
        decoded_body += chunk_data
        print(f"[Chunk] {chunk_size} bytes: {chunk_data.decode(errors='ignore')}")  # 打印 chunk 内容
    return decoded_body


def decompress_gzip(body):
    """解压 Gzip 响应体"""
    try:
        return gzip.decompress(body)
    except Exception as e:
        print(f"[x] Gzip 解压失败: {e}")
        return body  # 返回原始数据

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
    # if headers.get("Content-Encoding", "").lower() == "gzip":
    #     body = decompress_gzip(body)
    return status_line, headers, body

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
