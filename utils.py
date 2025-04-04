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


def extract_embedded_resources(html_body, base_url):
    """
    解析 HTML，提取所有嵌入资源的 URL（img/src、link/href、script/src）
    """
    resource_urls = set()

    # 正则匹配 src/href 属性
    resource_patterns = [
        r'<img[^>]+src=["\']([^"\']+)["\']',
        r'<link[^>]+href=["\']([^"\']+)["\']',
        r'<script[^>]+src=["\']([^"\']+)["\']'
    ]

    for pattern in resource_patterns:
        for match in re.findall(pattern, html_body, re.IGNORECASE):
            resource_urls.add(resolve_relative_url(base_url, match))

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

