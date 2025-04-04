import socket
import sys
import ssl

from uri_utils import parse_uri, get_host_port
from http_request import (
    build_get_request,
    build_head_request,
    build_post_request,
    inject_default_headers,
    build_multipart_form_data
)
from http_response import (
    read_response,
    is_redirect,
    get_redirect_location
)
from cookie_jar import CookieJar
from utils import save_to_file, extract_embedded_resources, resolve_relative_url
from cache import is_cached, get_cached_headers, store_response, load_cached_body

USER_AGENT = "XiongYuan and LiXinRui"
COOKIE_JAR = CookieJar()


def make_connection(host, port, use_https=False):
    """建立 HTTP/HTTPS 连接"""
    if use_https:
        port = port or 443
        context = ssl.create_default_context()
        try:
            raw_sock = socket.create_connection((host, port), timeout=5)
            sock = context.wrap_socket(raw_sock, server_hostname=host)  # SNI 支持
            return sock
        except ssl.SSLError as e:
            print(f"[SSL错误] {e}")
            raise
    else:
        port = port or 80
        return socket.create_connection((host, port), timeout=5)


def send_request(uri, method="GET", body=None, file_path=None, depth=0):
    """发送 HTTP/HTTPS 请求，支持缓存与重定向"""
    if depth > 5:
        print("[!] 重定向次数过多")
        return

    uri_parsed = parse_uri(uri)
    host, port = get_host_port(uri_parsed)

    headers = {}
    inject_default_headers(headers, host, keep_alive=False, user_agent=USER_AGENT)

    # 如果存在缓存，添加 `If-Modified-Since` 和 `If-None-Match` 头
    if is_cached(uri):
        cached_headers = get_cached_headers(uri)
        headers.update({k: v for k, v in cached_headers.items() if v})

    CookieJar.inject_into_headers(COOKIE_JAR, headers, uri)
    print("COOKIE_JAR:",COOKIE_JAR.getcookies())
    # 处理文件上传
    if method == "POST" and file_path:
        body, extra_headers = build_multipart_form_data(file_path)
        headers.update(extra_headers)

    # 构造请求
    if method == "GET":
        request = build_get_request(uri_parsed, headers)
    elif method == "HEAD":
        request = build_head_request(uri_parsed, headers)
    elif method == "POST":
        request = build_post_request(uri_parsed, body or "", headers, file_path)
    else:
        raise ValueError("Unsupported HTTP method")

    use_https = uri_parsed.scheme == "https"
    sock = make_connection(host, port, use_https=use_https)
    # 发送请求
    if isinstance(request, str):
        print("request:\n" + request)
        sock.sendall(request.encode("utf-8"))  # 仅字符串需要 encode
    else:
        print("request为bytes")
        sock.sendall(request)  # 如果已经是 bytes，直接发送

    status_line, headers, body = read_response(sock)
    sock.close()

    # 提取cookie

    COOKIE_JAR.extract_from_headers(headers)

    print(f"[i] {status_line}")
    print(f"[i] 响应头: {headers}")

    # 处理 304 Not Modified，直接返回缓存内容
    status_code = int(status_line.split()[1])
    if status_code == 304:
        print("[CACHE] 服务器返回 304 Not Modified，使用缓存")
        return load_cached_body(uri)

    # 处理重定向
    if is_redirect(status_code):
        location = get_redirect_location(headers)
        redirect_uri = resolve_relative_url(uri, location)
        print(f"[→] 重定向到 {redirect_uri}")
        return send_request(redirect_uri, method, body, depth + 1)

    # 存储缓存
    store_response(uri, headers, body)

    # 保存主页面
    save_to_file(uri_parsed, body, headers.get("Content-Type"))

    # 如果是 HTML 页面则提取资源并下载
    content_type = headers.get("Content-Type", "")
    if "text/html" in content_type and method == "GET":
        download_embedded_resources(body, uri)

    return body


def download_embedded_resources(html_body, base_uri):
    resources = extract_embedded_resources(html_body.decode(errors="ignore"), base_uri)
    print(f"[i] 共发现嵌入资源 {len(resources)} 个")

    # 递归下载内嵌资源
    for res_uri in resources:
        try:
            print(f"[↓] 下载资源: {res_uri}")
            send_request(res_uri, method="GET")
        except Exception as e:
            print(f"[x] 获取资源失败: {res_uri} ({e})")


def main():
    method = "POST"
    url = "http://47.109.192.71:8080/"  # 选择一个支持 POST 的服务器
    file_path = "post_file.txt"
    # if method == "POST" and file_path == None:
    #     import json
    #     data = json.dumps({"name": "Alice", "message": "Hello"})
    # else:
    #     data = None
    
    try:
        body = send_request(url, method=method, file_path=file_path)
        print("[响应体]:")
        print(body if body else "无返回内容")
    except Exception as e:
        print(f"[x] 请求失败: {e}")


if __name__ == "__main__":
    main()
