# Cookie管理
class CookieJar:
    def __init__(self):
        self.cookies = {}

    def extract_from_headers(self, headers):
        # 从 Set-Cookie 提取并存入 self.cookies
        pass

    def inject_into_headers(self, headers):
        # 添加 Cookie 字段到 headers 中
        pass
