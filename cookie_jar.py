# Cookie管理
import re
import time
from urllib.parse import urlparse

class CookieJar:
    def __init__(self):
        """初始化 Cookie 存储"""
        self.cookies = {}

    def extract_from_headers(self, headers):
        """
        从 HTTP 响应头中提取 `Set-Cookie` 并存储
        :param headers: 服务器返回的 HTTP 响应头 (dict)
        """
        if "Set-Cookie" not in headers:
            return

        # 兼容多行 Set-Cookie
        set_cookie_headers = headers.get_all("Set-Cookie") if hasattr(headers, "get_all") else [headers["Set-Cookie"]]

        for cookie_str in set_cookie_headers:
            self._parse_cookie(cookie_str)

    def _parse_cookie(self, cookie_str):
        """
        解析 `Set-Cookie` 头，并存入 self.cookies
        :param cookie_str: 单个 `Set-Cookie` 头的值
        """
        parts = cookie_str.split(";")
        main_part = parts[0].strip()
        key, value = main_part.split("=", 1)
        cookie_data = {
            "value": value.strip(),
            "expires": None,
            "path": "/",
            "domain": None,
            "secure": False,
            "httpOnly": False
        }

        # 解析属性
        for attr in parts[1:]:
            attr = attr.strip().lower()
            if attr.startswith("expires="):
                cookie_data["expires"] = self._parse_expires(attr[len("expires="):])
            elif attr.startswith("path="):
                cookie_data["path"] = attr[len("path="):].strip()
            elif attr.startswith("domain="):
                cookie_data["domain"] = attr[len("domain="):].strip()
            elif attr == "secure":
                cookie_data["secure"] = True
            elif attr == "httponly":
                cookie_data["httpOnly"] = True

        # 存储 Cookie
        self.cookies[key] = cookie_data

    def _parse_expires(self, expires_str):
        """
        解析 `expires` 过期时间，转换为时间戳
        """
        try:
            return time.mktime(time.strptime(expires_str, "%a, %d-%b-%Y %H:%M:%S GMT"))
        except ValueError:
            return None

    def inject_into_headers(self, headers, url):
        """
        在请求头中添加 `Cookie` 以保持会话
        :param headers: 要修改的 HTTP 请求头 (dict)
        :param url: 当前请求的 URL（用于匹配域名和路径）
        """
        parsed_url = urlparse(url)
        domain = parsed_url.hostname
        path = parsed_url.path or "/"

        cookie_header = []
        current_time = time.time()

        for key, cookie in self.cookies.items():
            # 过滤掉不匹配域名、路径或已过期的 Cookie
            if (cookie["domain"] and cookie["domain"] not in domain) or not path.startswith(cookie["path"]):
                continue

            if cookie["expires"] and cookie["expires"] < current_time:
                continue  # 过期 Cookie 不发送

            cookie_header.append(f"{key}={cookie['value']}")

        if cookie_header:
            headers["Cookie"] = "; ".join(cookie_header)
