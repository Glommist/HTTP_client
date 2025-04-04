import socket
import gzip
# from test_request import send_http_request  # 假设你有一个发送 HTTP 请求的函数
from http_response import read_response  # 你的 HTTP 响应解析函数
def is_gzipped(data):
    return data[:2] == b'\x1f\x8b'  # Gzip 文件的 magic bytes

def test_gzip():
    host = "httpbin.org"
    port = 80  # HTTP 默认端口
    request = (
        "GET /gzip HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        "User-Agent: CustomClient/1.0\r\n"
        "Accept-Encoding: gzip\r\n"  # 明确请求 gzip 压缩
        "Connection: close\r\n\r\n"
    )

    # 创建 Socket 连接
    with socket.create_connection((host, port)) as sock:
        sock.sendall(request.encode())

        # 解析 HTTP 响应
        status_line, headers, body = read_response(sock)

    # 输出解析结果
    print("[i] HTTP 状态行:", status_line)
    print("[i] 响应头:", headers)

    # 验证是否是 gzip 压缩
    if headers.get("Content-Encoding", "").lower() == "gzip":
        print("[✓] 响应是 gzip 压缩的")
        try:
            if is_gzipped(body):
                decompressed_body = gzip.decompress(body)
                print("[✓] 解压成功，内容如下：")
                print(decompressed_body.decode("utf-8", errors="ignore"))
            else:
                print("[x] 服务器返回的内容 **并未** 经过 gzip 压缩，可能是服务器错误地标记了 Content-Encoding。")
                print("[i] 原始响应体如下：")
                print(body.decode("utf-8", errors="ignore"))
        except Exception as e:
            print("[x] Gzip 解压失败:", e)
    else:
        print("[x] 服务器未返回 gzip 响应")

if __name__ == "__main__":
    test_gzip()
