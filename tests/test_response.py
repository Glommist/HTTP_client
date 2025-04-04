# 测试 chunked, gzip 解析等
import unittest
from io import BytesIO
import socket
import gzip
from http_response import (
    read_response,
    handle_chunked_body,
    decompress_gzip,
    is_redirect,
    get_redirect_location
)


class MockSocket:
    """用于模拟 socket.recv() 的行为"""
    def __init__(self, response_data):
        self.stream = BytesIO(response_data)

    def recv(self, bufsize):
        return self.stream.read(bufsize)


class TestHTTPResponse(unittest.TestCase):
    def test_read_response(self):
        """测试解析 HTTP 响应"""
        raw_response = (
            b"HTTP/1.1 200 OK\r\n"
            b"Content-Length: 13\r\n"
            b"Connection: close\r\n"
            b"\r\n"
            b"Hello, World!"
        )
        mock_sock = MockSocket(raw_response)
        status_line, headers, body = read_response(mock_sock)

        self.assertEqual(status_line, "HTTP/1.1 200 OK")
        self.assertEqual(headers["Content-Length"], "13")
        self.assertEqual(body, b"Hello, World!")

    def test_handle_chunked_body(self):
        """测试 Chunked 传输解析"""
        chunked_response = (
            b"4\r\nWiki\r\n"
            b"5\r\npedia\r\n"
            b"0\r\n\r\n"
        )
        mock_sock = MockSocket(chunked_response)
        body = handle_chunked_body(b"", mock_sock)
        self.assertEqual(body, b"Wikipedia")

    def test_decompress_gzip(self):
        """测试 Gzip 解压"""
        original_data = b"Hello, Gzip!"
        gzip_buffer = BytesIO()
        with gzip.GzipFile(fileobj=gzip_buffer, mode="wb") as f:
            f.write(original_data)

        compressed_data = gzip_buffer.getvalue()
        decompressed_data = decompress_gzip(compressed_data)

        self.assertEqual(decompressed_data, original_data)

    def test_is_redirect(self):
        """测试是否是重定向"""
        self.assertTrue(is_redirect(301))
        self.assertTrue(is_redirect(302))
        self.assertFalse(is_redirect(200))
        self.assertFalse(is_redirect(404))

    def test_get_redirect_location(self):
        """测试获取重定向地址"""
        headers = {"Location": "https://www.xjtu.edu.cn/"}
        self.assertEqual(get_redirect_location(headers), "https://www.xjtu.edu.cn/")

        headers = {}
        self.assertIsNone(get_redirect_location(headers))


if __name__ == "__main__":
    unittest.main()
