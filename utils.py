# 工具函数
import os
import re


def save_to_file(uri, body_bytes, content_type=None):
    """
    根据 URI 和 Content-Type 推测文件名，并保存数据到本地文件
    """
    # 提取文件名
    path = uri.path
    filename = os.path.basename(path) or "index.html"

    # 确定扩展名
    if not os.path.splitext(filename)[1] and content_type:
        ext_map = {
            "text/html": ".html",
            "text/plain": ".txt",
            "application/json": ".json",
            "image/jpeg": ".jpg",
            "image/png": ".png",
            "image/gif": ".gif",
            "text/css": ".css",
            "application/javascript": ".js",
        }
        filename += ext_map.get(content_type.split(";")[0], "")

    # 确保目录存在
    os.makedirs("downloaded", exist_ok=True)
    filepath = os.path.join("downloaded", filename)

    # 保存文件
    with open(filepath, "wb") as f:
        f.write(body_bytes)

    print(f"[✓] Saved: {filepath}")

from urllib.parse import urljoin

def extract_embedded_resources(html_body, base_url, resource_types=None):
    """
    从 HTML 中提取指定类型的嵌入资源 URL
    支持的类型包括：'img', 'link', 'script', 'pdf'

    参数：
    - html_body: HTML 内容字符串
    - base_url: 用于转换相对路径为绝对路径
    - resource_types: 要提取的资源类型列表，默认全部提取
    """
    resource_urls = set()

    all_patterns = {
        'img': r'<img[^>]+src=["\']([^"\']+)["\']',
        'link': r'<link[^>]+href=["\']([^"\']+)["\']',
        'script': r'<script[^>]+src=["\']([^"\']+)["\']',
        'pdf': r'<a[^>]+href=["\']([^"\']+\.pdf(?:\?[^"\']*)?)["\']'
    }

    # 如果未指定类型，则默认提取所有支持的资源
    selected_patterns = all_patterns if resource_types is None else {
        k: v for k, v in all_patterns.items() if k in resource_types
    }

    for key, pattern in selected_patterns.items():
        matches = re.findall(pattern, html_body, re.IGNORECASE)
        for match in matches:
            resource_urls.add(urljoin(base_url, match))

    return list(resource_urls)


def resolve_relative_url(base, relative):
    """
    解析相对 URL，转换成完整的绝对 URL
    """
    if relative.startswith("http://") or relative.startswith("https://"):
        return relative

    # 处理 `//example.com/path`
    if relative.startswith("//"):
        return base.split(":")[0] + ":" + relative

    # 提取 base URL 结构
    match = re.match(r"^(https?://[^/]+)(/.*)?$", base)
    if not match:
        raise ValueError(f"Invalid base URL: {base}")

    base_domain, base_path = match.groups()
    base_path = base_path or "/"

    # 处理以 `/` 开头的相对路径（根路径）
    if relative.startswith("/"):
        return base_domain + relative

    # 处理 `../` 和 `./`
    base_parts = base_path.rstrip("/").split("/")
    relative_parts = relative.split("/")

    while relative_parts and relative_parts[0] in ("..", "."):
        if relative_parts[0] == "..":
            if len(base_parts) > 1:
                base_parts.pop()
        relative_parts.pop(0)

    new_path = "/".join(base_parts + relative_parts)
    return base_domain + "/" + new_path.lstrip("/")

