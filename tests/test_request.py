# 测试 request 构造是否符合规范
import socket

from http_request import build_get_request


def send_http_request(request, host, port=80):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(request.encode())
        response = b""
        while True:
            chunk = s.recv(4096)  # 一次读取 4KB
            if not chunk:
                break
            response += chunk

    return response.decode(errors="ignore")  # 忽略解码错误

# 发送 GET 请求
url = "https://www.xjtu.edu.cn/"
request = build_get_request(url)
response = send_http_request(request, "www.xjtu.edn.cn")
print(response)
