# 处理URI的%编码、解析host/port/path
from urllib.parse import urlparse, unquote

def parse_uri(uri_str):
    # 返回 urllib.parse.ParseResult 对象
    pass

def get_host_port(uri):
    # 返回 (host, port)
    pass

def normalize_path(path):
    # 解码 %7E 等字符
    pass
