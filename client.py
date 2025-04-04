# 主程序

import socket
import sys

from uri_utils import parse_uri, get_host_port
from http_request import (
    build_get_request,
    build_head_request,
    build_post_request,
    inject_default_headers
)
from http_response import (
    read_response,
    is_redirect,
    get_redirect_location
)
from cookie_jar import CookieJar
from utils import save_to_file, extract_embedded_resources, resolve_relative_url


USER_AGENT = "YourName"  
COOKIE_JAR = CookieJar()


def make_connection(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    return sock


def send_request(uri, method="GET", body=None, depth=0):
    if depth > 5:
        print("[!] 重定向次数过多")
        return

    uri_parsed = parse_uri(uri)
    host, port = get_host_port(uri_parsed)

    headers = {}
    inject_default_headers(headers, host, keep_alive=False, user_agent=USER_AGENT)
    COOKIE_JAR.inject_into_headers(headers)

    # 构造请求
    if method == "GET":
        request = build_get_request(uri_parsed, headers)
    elif method == "HEAD":
        request = build_head_request(uri_parsed, headers)
    elif method == "POST":
        request = build_post_request(uri_parsed, body or "", headers)
    else:
        raise ValueError("Unsupported HTTP method")

    sock = make_connection(host, port)
    sock.sendall(request)

    status_line, headers, body = read_response(sock)
    sock.close()

    print(f"[i] {status_line}")
    print(f"[i] 响应头: {headers.get('Content-Type', '')}")

    COOKIE_JAR.extract_from_headers(headers)

    # 重定向处理
    status_code = int(status_line.split()[1])
    if is_redirect(status_code):
        location = get_redirect_location(headers)
        redirect_uri = resolve_relative_url(uri, location)
        print(f"[→] 重定向到 {redirect_uri}")
        return send_request(redirect_uri, method, body, depth + 1)

    # 保存主页面
    save_to_file(uri, body, headers.get("Content-Type"))

    # 如果是 HTML 页面则提取资源并下载
    content_type = headers.get("Content-Type", "")
    if "text/html" in content_type and method == "GET":
        download_embedded_resources(body, uri)

    return body


def download_embedded_resources(html_body, base_uri):
    resources = extract_embedded_resources(html_body.decode(errors="ignore"), base_uri)
    print(f"[i] 共发现嵌入资源 {len(resources)} 个")

    for res_uri in resources:
        try:
            print(f"[↓] 下载资源: {res_uri}")
            send_request(res_uri, method="GET")
        except Exception as e:
            print(f"[x] 获取资源失败: {res_uri} ({e})")


def main():
    if len(sys.argv) < 3:
        print("Usage: python client.py <METHOD> <URL> [POST_DATA]")
        return

    method = sys.argv[1].upper()
    url = sys.argv[2]
    data = sys.argv[3] if method == "POST" and len(sys.argv) > 3 else None

    try:
        send_request(url, method=method, body=data)
    except Exception as e:
        print(f"[x] 请求失败: {e}")


if __name__ == "__main__":
    main()

