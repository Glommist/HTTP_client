# 测试 URL 解析与编码处理
from uri_utils import parse_uri, normalize_path


def test_parse_uri():
    test_cases = [
        {
            "uri": "http://example.com/index.html",
            "expected": {
                "scheme": "http",
                "host": "example.com",
                "port": 80,
                "path": "/index.html",
                "query": "",
                "full_path": "/index.html"
            }
        },
        {
            "uri": "http://abc.com:8080/~user/file.txt?debug=true",
            "expected": {
                "scheme": "http",
                "host": "abc.com",
                "port": 8080,
                "path": "/~user/file.txt",
                "query": "debug=true",
                "full_path": "/~user/file.txt?debug=true"
            }
        },
        {
            "uri": "http://ABC.com/%7Esmith/",
            "expected": {
                "scheme": "http",
                "host": "abc.com",  # 小写处理
                "port": 80,
                "path": "/~smith/",
                "query": "",
                "full_path": "/~smith/"
            }
        },
    ]

    for i, case in enumerate(test_cases):
        uri = parse_uri(case["uri"])
        exp = case["expected"]
        assert uri.scheme == exp["scheme"], f"Test {i+1} failed: scheme"
        assert uri.host == exp["host"], f"Test {i+1} failed: host"
        assert uri.port == exp["port"], f"Test {i+1} failed: port"
        assert uri.path == exp["path"], f"Test {i+1} failed: path"
        assert uri.query == exp["query"], f"Test {i+1} failed: query"
        assert uri.full_path() == exp["full_path"], f"Test {i+1} failed: full_path"
        print(f"[✓] Test {i+1} passed.")

def test_normalize_path():
    assert normalize_path("/%7Esmith/test") == "/~smith/test"
    assert normalize_path("/a%2Fb") == "/a/b"
    assert normalize_path("/%41%42%43") == "/ABC"
    print("[✓] normalize_path tests passed.")


if __name__ == "__main__":
    test_parse_uri()
    test_normalize_path()
