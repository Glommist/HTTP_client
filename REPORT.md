# 🌐 计算机网络专题实验 - 实验八报告

<table style="width:100%">
  <tr>
    <th>👤 姓名</th>
    <th>🏫 班级</th>
  </tr>
  <tr>
    <td>熊原</td>
    <td>计算机2201</td>
  </tr>
  <tr>
    <td>李鑫瑞</td>
    <td>计算机2204</td>
  </tr>
</table>

---

## 🧪 一、实验名称  

### 📄 基于 **HTTP** 协议的客户端程序（文本浏览器）

---

## 🧠 二、实验原理  

- **🔁 TCP 原理**：
   建立连接需三次握手，关闭连接需四次挥手。通过序列号、确认应答、窗口控制和重传机制，确保数据可靠有序传输。同时采用流量控制和拥塞控制优化网络传输。

- **🔗 C/S 模式工作原理**：
  - **🖥️ 服务器端**：
    创建 Socket → 绑定端口 → 监听连接 → 接受客户端 → 通信 → 验证用户信息 → 返回验证结果 → 关闭连接

  - **💻 客户端**：
    创建 Socket → 发起连接 → 输入用户名密码 → 等待验证 → 通信完成 → 主动关闭连接

---

## 🎯 三、实验目的  

1. 💡 握**Sockets**的相关基础知识，学习**Sockets**编程的基本函数和模式、框架。  
2. 📡 掌握**UDP**、**TCP**协议及**Client/Server**和**P2P**两种模式的通信原理。掌握可靠数据传输协议（**GBN**和**SR**协议）  
3. 🔧 掌握 socket 编程框架

---

## 📚 四、实验内容  

### ✅ 1. 基本功能  

- 客户端程序基于标准的**HTTP/1.1**协议（**RFC 2616**等），能够把请求得到的资源保存在本地的文件中。

#### 📌 基本要求：

- 🔘 支持**GET**、**HEAD**和**POST**三种请求方法，支持**URI**的"**%HEXHEX**"编码，如对 **http://abc.com:80/~smith/** 和 **http://ABC.com/%7Esmith/** 两种等价的**URI** 能够正确处理；支持**Connection: Keep-Alive**和**Connection: Close**两种连接模式；
- 🔗  能够把一个网页中所有的内嵌对象（如**HTML**中的**IMG**、**CSS**、**JS**等对象）一次全部获取；
- 🍪 支持**Cookie**（见**RFC 2109**）的基本机制，实现典型的网站登录；
- 📥 能够正确处理几种典型的应答（如**200**，**100**，**301**，**304**，**404**，**500**等），并支持重定向请求；
- 📁 支持基础缓存机制

### 🚀 2. 高级功能  

- 🔐 支持**HTTPS**；
- 🧩 支持分块传输编码(**Chunked Transfer Encoding**)、**gzip**等内容编码；
- 📤 支持基于**POST**方法的文件上传；
- 🎯 支持把一个网页中特定对象（如多个**PDF**资源）一次全部获取。

---

## 🔧 五、实验实现  

### 👥 1. 人员分工  
*（此部分可根据实际补充）*

### 🧩 2. 实验设计  

#### 🔗 协议
- 本实验采用 **TCP + C/S** 通信模型，客户端通过 socket 与服务器建立连接，发送 HTTP 请求并解析响应。使用多线程或异步实现多用户通信，必要时对共享资源加锁保护。

#### 🖼️ UI设计  
![ui](report/picture/ui.png)  
  设计如上：我们支持了请求方法（**GET** **HEAD** **POST**）的选择，支持输入URL以进行访问，在请求方法为**POST**时间，支持在本地文件中选择需要上传的文件，同时支持选择文件类型来协助文件上传。在返回部分，我们设计了**状态行**，**响应头**，**响应体**三个返回框，可以在用户发送请求后，返回**HTTP**报文的返回状态，响应头，和原始的响应体内容。

#### 🏗️ 框架结构  
我们的项目结构如下:
```
HTTP_CLIENT
│  cache.py
│  client.py
│  cookie_jar.py
│  http_request.py
│  http_response.py
│  uri_utils.py
│  utils.py
│
├─report
│  └─picture
│        └─ui.png
│
├─tests
│  │  test_cache.py
│  │  test_chunked.py
│  │  test_cookie.py
│  │  test_gzip.py
│  │  test_request.py
│  │  test_response.py
│  └─ test_uri.py
│   
│  
│
└─ui
   │  http_ui.py
   │
   └─picture
          Arrow-down.svg
          icon.png
```

#### 📦 模块说明

| 模块文件名         | 功能描述                                                                 |
|--------------------|--------------------------------------------------------------------------|
| **`client.py`**        | 项目的核心模块，负责建立 **`HTTP/HTTPS`** 连接构造请求、发送请求、接收响应、处理缓存、重定向、Cookie、资源下载等。 |
| **`http_request.py`** | 提供 **GET / HEAD / POST** 请求报文的构造函数，支持文件上传、表单编码等。         |
|**`http_response.py`** | 解析响应报文，提取状态行、响应头和响应体，支持分块传输 **(** **chunked** **)** 、**gzip** 解压等，同时支持判断**HTTP**状态码是否为重定向，也支持获取重定向的**URL**|
| **`cookie_jar.py`**    | 管理 **Cookie** 的存储与生命周期，实现从响应中提取和向请求头中注入 **Cookie**。         |
| **`cache.py`**         | 实现简单的缓存机制，支持根据URL计算缓存文件的路径，可以判断URL是否存在缓存，支持获取缓存的 **`Last-Modified`** 和 **`ETag`**，用于 **`If-Modified-Since / If-None-Match`**，支持存储 **`HTTP`** 响应到缓存，同时也支持从缓存加载响应体 |
| **`uri_utils.py`**     | 实现 **URI** 的解析、标准化，确保资源定位和处理正确。      |
| **`utils.py`**        | 存放通用工具函数，例如文件保存、路径生成、类型判断、编码处理，解析相对 **`URL`**，转换成完整的绝对 **`URL`**。     

#### 🖼️ UI 模块说明

| 模块/目录           | 功能描述                                                                |
|----------------------|-------------------------------------------------------------------------|
|**`ui/http_ui.py`**      | 图形化用户界面主程序，使用 **PyQt5** 实现功能选择、**URL** 输入、响应展示。 |
| **`ui/picture/`**        | 存放图形界面所使用的图标与资源图片。                                     |

#### 🧪 测试模块说明

| 测试脚本             | 测试内容                                                         |
|----------------------|------------------------------------------------------------------|
| **`test_cache.py`**      | 测试缓存模块的读写、条件缓存请求 **（** **If-Modified-Since** **）**逻辑。        |
| **`test_chunked.py`**   | 测试分块传输 **（** **Chunked Transfer Encoding** **）** 内容的解析正确性。       |
| **`test_cookie.py`**     | 测试 **Cookie** 的注入与提取机制。          |
| **`test_gzip.py`**       | 测试在显性设置以**gzip**形式传输报文的情况下是否能正常传输和解压缩                 |
| **`test_request.py`**    | 测试**GET**是否能够正常执行，以此确定URL的解析是否正确 |
| **`test_response.py`**   |测试**HTTP**响应能否正常解析，测试获取重定向地址。    |
| **`test_uri.py`**        | 测试 **URI** 工具函数的解析、重定向地址拼接、编码/解码等功能。

---

### 💻**3**. 关键代码的描述  

#### （**一**） 关键代码**1**:
##### 🔧 send_request
自主编写：大部分由熊原编写，李鑫瑞做了部分修改和添加
```python
def send_request(uri, method="GET", body=None, file_path=None, depth=0, resource_types=None):
    """发送 HTTP/HTTPS 请求，支持缓存与重定向"""
    if depth > 5:
        print("[!] 重定向次数过多")
        return

    uri_parsed = parse_uri(uri)
    host, port = get_host_port(uri_parsed)

    headers = {}
    inject_default_headers(headers, host, keep_alive=False, user_agent=USER_AGENT)

    # 如果存在缓存，添加 `If-Modified-Since` 和 `If-None-Match` 头
    if is_cached(uri):
        cached_headers = get_cached_headers(uri)
        headers.update({k: v for k, v in cached_headers.items() if v})

    CookieJar.inject_into_headers(COOKIE_JAR, headers, uri)
    print("COOKIE_JAR:",COOKIE_JAR.getcookies())
    # 处理文件上传
    if method == "POST" and file_path:
        body, extra_headers = build_multipart_form_data(file_path)
        headers.update(extra_headers)

    # 构造请求
    if method == "GET":
        request = build_get_request(uri_parsed, headers)
    elif method == "HEAD":
        request = build_head_request(uri_parsed, headers)
    elif method == "POST":
        request = build_post_request(uri_parsed, body or "", headers, file_path)
    else:
        raise ValueError("Unsupported HTTP method")

    use_https = uri_parsed.scheme == "https"
    sock = make_connection(host, port, use_https=use_https)
    # 发送请求
    if isinstance(request, str):
        print("request:\n" + request)
        sock.sendall(request.encode("utf-8"))  # 仅字符串需要 encode
    else:
        print("request为bytes")
        sock.sendall(request)  # 如果已经是 bytes，直接发送

    status_line, headers, body = read_response(sock)
    sock.close()

    if method == "HEAD":
        body = None

    # 提取cookie

    COOKIE_JAR.extract_from_headers(headers)
    
    # 处理 304 Not Modified，直接返回缓存内容
    status_code = int(status_line.split()[1])
    if status_code == 304:
        print("[CACHE] 服务器返回 304 Not Modified，使用缓存")
        if method == "HEAD":
            return status_line,get_cached_headers(uri),None
        return status_line,get_cached_headers(uri),load_cached_body(uri)


    # 处理重定向
    if is_redirect(status_code):
        location = get_redirect_location(headers)
        redirect_uri = resolve_relative_url(uri, location)
        print(f"[→] 重定向到 {redirect_uri}")
        return status_line,headers,send_request(redirect_uri, method, body, depth + 1, resource_types=resource_types)

    # 存储缓存
    store_response(uri, headers, body)

    # 保存主页面
    save_to_file(uri_parsed, body, headers.get("Content-Type"))

    # 如果是 HTML 页面则提取资源并下载
    content_type = headers.get("Content-Type", "")
    if "text/html" in content_type and method == "GET":
        download_embedded_resources(body, uri, resource_types=resource_types)

    return status_line,headers,body

```
该部分具有以下功能：
- 支持 **GET/HEAD/POST** 三种 HTTP 方法

- 处理文件上传 **（POST）**

- 支持 **Cookie**、缓存、重定向

- 可以自动下载 **HTML** 中嵌套的资源（如 **CSS**、**JS**、图片）

- 支持最大重定向深度控制

#### （**二**） 关键代码**2**
##### 🔧 parse_uri
自主编写：由熊原编写
```python
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
        if scheme == 'http':
            port = 80
        if scheme == 'https':
            port = 443

    # 4. 提取 path 和 query
    if "?" in path_query:
        path, query = path_query.split("?", 1)
    else:
        path = path_query
        query = ""

    return URI(scheme, host.lower(), port, normalize_path(path), query)
```
该部分具有以下功能：
- 拆解 **scheme://host:port/path?query** 格式**URI**

- 默认端口设置：**http=80，https=443**

- 为后续构造请求做准备（尤其用于分离主机与路径）



#### （**三**） 关键代码**3**
##### 🔧 GET HEAD POST
自主编写：由李鑫瑞编写
```python
# 构造 GET 请求
def build_get_request(uri, headers=None):
    path = uri.path or "/"
    if uri.query:
        path += f"?{uri.query}"

    request_line = f"GET {path} HTTP/1.1"
    default_headers = {
        "Host": uri.host,
        "User-Agent": "XiongYuan and LiXinRui",
        "Connection": "Keep-Alive"
    }

    if headers:
        default_headers.update(headers)

    headers_str = "\r\n".join(f"{key}: {value}" for key, value in default_headers.items())
    return f"{request_line}\r\n{headers_str}\r\n\r\n"


# 构造 HEAD 请求（同 GET，但无 Body）
def build_head_request(uri, headers=None):
    path = uri.path or "/"
    if uri.query:
        path += f"?{uri.query}"

    request_line = f"HEAD {path} HTTP/1.1"
    default_headers = {
        "Host": uri.host,
        "User-Agent": "XiongYuan and LiXinRui",
        "Connection": "Keep-Alive"
    }

    if headers:
        default_headers.update(headers)

    headers_str = "\r\n".join(f"{key}: {value}" for key, value in default_headers.items())
    return f"{request_line}\r\n{headers_str}\r\n\r\n"


# 构造 POST 请求
def build_post_request(uri, data, headers=None, file_path=None):
    path = uri.path or "/"
    if uri.query:
        path += f"?{uri.query}"

    request_line = f"POST {path} HTTP/1.1"

    default_headers = {
        "Host": uri.host,
        "User-Agent": "XiongYuan and LiXinRui",
        "Connection": "Keep-Alive"
    }

    # 处理 JSON 数据
    if data and not file_path:
        body = json.dumps(data)
        default_headers["Content-Type"] = "application/json"
        default_headers["Content-Length"] = str(len(body))

    # 处理文件上传
    elif file_path:
        boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
        file_name = os.path.basename(file_path)
        mime_type = mimetypes.guess_type(file_name)[0] or "application/octet-stream"

        with open(file_path, "rb") as f:
            file_content = f.read()

        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="file"; filename="{file_name}"\r\n'
            f"Content-Type: {mime_type}\r\n\r\n"
        ).encode() + file_content + f"\r\n--{boundary}--\r\n".encode()

        default_headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"
        default_headers["Content-Length"] = str(len(body))

    else:
        raise ValueError("POST 请求需要提供 data 或 file_path")

    # 合并用户自定义 Headers
    if headers:
        default_headers.update(headers)

    headers_str = "\r\n".join(f"{key}: {value}" for key, value in default_headers.items())
    
    # 如果是 JSON，则返回字符串；如果是文件上传，则返回二进制数据
    if file_path:
        request = f"{request_line}\r\n{headers_str}\r\n\r\n".encode() + body
    else:
        request = f"{request_line}\r\n{headers_str}\r\n\r\n{body}"

    return request

```
该部分具有以下功能：
- 三个函数分别构建 **GET / HEAD / POST** 请求报文

- 支持手动追加 **Headers**，如 **User-Agent Connection**

- **POST** 支持上传 **JSON** 数据 和 文件（表单 **multipart** 上传）

- 文件上传时自动判断 **MIME** 类型



#### （**四**） 关键代码**4**
##### 🔧 chunked Gzip
自主编写：李鑫瑞编写
```python
def handle_chunked_body(body, sock):
    decoded_body = b""
    while True:
        chunk_size_line = read_line(sock)
        try:
            chunk_size = int(chunk_size_line, 16)  # 16 进制解析 chunk 大小
        except ValueError:
            print(f"Skipping invalid chunk size: {repr(chunk_size_line)}")
            continue  # 跳过无效的 chunk size
        if chunk_size == 0:
            break  # 结束处理
        chunk_data = recv_exact(sock, chunk_size)
        sock.recv(2)  # 读取 \r\n
        decoded_body += chunk_data
        print(f"[Chunk] {chunk_size} bytes: {chunk_data.decode(errors='ignore')}")  # 打印 chunk 内容
    return decoded_body


def decompress_gzip(body):
    """解压 Gzip 响应体"""
    try:
        return gzip.decompress(body)
    except Exception as e:
        print(f"[x] Gzip 解压失败: {e}")
        return body  # 返回原始数据
```
该部分具有以下功能：
- `handle_chunked_body` 用于逐块解析 **chunked** 编码响应体，自动跳过非法块

- `decompress_gzip` 解压 **Gzip** 编码的内容，自动降级处理异常



#### （**五**） 关键代码**5**
##### 🔧 cache
自主编写：由熊原编写
```python
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
```
该部分具有以下功能：
- 使用本地缓存目录保存请求响应的 **ETag / Last-Modified / Body**

- 可通过请求头 **If-Modified-Since** 和 **If-None-Match** 实现 **HTTP** 缓存机制

- 节省流量、提升响应速度
---

## 六、测试及结果分析  
*【测试过程应当比较详尽，把所有的功能都测试覆盖了，还要注意错误情况的处理。】*

### **1**. 测试**1**  
测试过程、说明、结果及分析。

### **2**. 测试**2**  
测试过程、说明、结果及分析。

---

## 七、实验结论  

---

## 八、总结及心得体会  

---

## 附件  
**1**. 源码文件  
[github地址](https://github.com/Glommist/HTTP_client.git)
**2**. 相关文档  
**3**. 参考资料（链接）……


