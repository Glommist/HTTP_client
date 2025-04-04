# 处理URI的%编码、解析host/port/path
import re


class URI:
    def __init__(self, scheme, host, port, path, query):
        self.scheme = scheme
        self.host = host
        self.port = port
        self.path = path or "/"
        self.query = query

    def full_path(self):
        return self.path + (f"?{self.query}" if self.query else "")


def parse_uri(uri_str):
    """
    手动解析 URI 字符串，返回 URI 对象
    支持 http://host:port/path?query
    """
    uri_str = uri_str.strip()

    # 1. 提取 scheme
    if "://" not in uri_str:
        raise ValueError("URI 缺少 scheme")
    scheme, rest = uri_str.split("://", 1)

    # 2. 提取 host[:port]
    path_start = rest.find("/")
    if path_start == -1:
        host_port = rest
        path_query = ""
    else:
        host_port = rest[:path_start]
        path_query = rest[path_start:]

    # 3. 提取 host 和 port
    if ":" in host_port:
        host, port_str = host_port.split(":", 1)
        port = int(port_str)
    else:
        host = host_port
        port = 443 if scheme == "https" else 80  # 默认端口

    # 4. 提取 path 和 query
    if "?" in path_query:
        path, query = path_query.split("?", 1)
    else:
        path = path_query
        query = ""

    return URI(scheme, host.lower(), port, normalize_path(path), query)


def get_host_port(uri):
    return uri.host, uri.port


def normalize_path(path):
    """
    解码 URI 中的 %HEXHEX，例如 %7E -> ~
    """
    def decode_match(match):
        hex_code = match.group(1)
        return chr(int(hex_code, 16))

    return re.sub(r'%([0-9A-Fa-f]{2})', decode_match, path)

