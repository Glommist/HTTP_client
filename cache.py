# 缓存机制实现
import os
import json
import hashlib
from datetime import datetime

CACHE_DIR = "cache_picture"

# 确保缓存目录存在
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)


def _get_cache_path(uri):
    """基于 URI 计算缓存文件路径"""
    hashed_uri = hashlib.md5(uri.encode()).hexdigest()
    return os.path.join(CACHE_DIR, hashed_uri)


def is_cached(uri):
    """判断 URI 是否有缓存"""
    cache_path = _get_cache_path(uri)
    return os.path.exists(cache_path)


def get_cached_headers(uri):
    """获取缓存的 `Last-Modified` 和 `ETag`，用于 If-Modified-Since / If-None-Match"""
    cache_path = _get_cache_path(uri)
    
    if not os.path.exists(cache_path):
        return {}

    with open(cache_path, "r", encoding="utf-8") as f:
        cache_data = json.load(f)

    return {
        "If-Modified-Since": cache_data.get("Last-Modified"),
        "If-None-Match": cache_data.get("ETag"),
    }



def store_response(uri, headers, body):
    """存储 HTTP 响应到缓存"""
    cache_path = _get_cache_path(uri)
    os.makedirs(os.path.dirname(cache_path), exist_ok=True)

    cache_data = {
        "Last-Modified": headers.get("Last-Modified"),
        "ETag": headers.get("ETag"),
        "Date": headers.get("Date"),
        "Body": body.decode("utf-8", errors="ignore"),  # 转换为字符串
    }

    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(cache_data, f, indent=4)


def load_cached_body(uri):
    """从缓存加载响应体"""
    cache_path = _get_cache_path(uri)
    with open(cache_path, "r", encoding="utf-8") as f:
        cache_data = json.load(f)

    return cache_data["Body"].encode("utf-8")

