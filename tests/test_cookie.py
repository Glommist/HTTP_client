# 测试 cookie 提取/注入
from client import send_request, COOKIE_JAR


def test_cookie_handling():
    # 第一步：访问 /cookies/set?session_id=123456 来让服务器返回 Set-Cookie
    print("\n[TEST] 发送请求以设置 Cookie")
    send_request("http://httpbin.org/cookies/set?session_id=123456")

    # 检查 CookieJar 是否存储了 session_id
    print("\n[TEST] 检查 CookieJar 是否存储了 session_id")
    print(f"当前 CookieJar 内容: {COOKIE_JAR.cookies}")

    # 第二步：访问 /cookies 检查服务器是否收到 Cookie
    print("\n[TEST] 发送请求以获取服务器存储的 Cookie")
    send_request("http://httpbin.org/cookies")

test_cookie_handling()
