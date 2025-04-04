# 解析响应，处理重定向、chunked等
def read_response(sock) -> tuple:
    # 返回 status_line, headers_dict, body_bytes
    pass

def handle_chunked_body(body_bytes, sock):
    pass

def decompress_gzip(body_bytes):
    pass

def is_redirect(status_code):
    pass

def get_redirect_location(headers):
    pass
