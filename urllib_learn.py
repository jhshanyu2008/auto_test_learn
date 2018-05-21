"""
学习资料来源： http://www.cnblogs.com/zhaof/p/6910871.html
博客作者：python修行路
"""
import socket  # 网络信息模块
import http.cookiejar  # 获取和储存cookie
import urllib.request  # 请求模块
import urllib.parse  # url解析模块
import urllib.error  # 错误处理模块


# ————————————————request.urlopen 三个基本参数：url地址,post数据，超时时间————————————————— #
def urllib_request_urlopen_get_test():
    # 没有其他参数，默认使用一次get请求
    response = urllib.request.urlopen('http://www.baidu.com')
    print(response.read().decode('utf-8'))


def urllib_request_urlopen_post_test():
    data = bytes(urllib.parse.urlencode({'word': 'hello'}), encoding='utf8')
    print(data)
    # 将post数据进行转换放到data参数中,这样就完成了一次post请求
    response = urllib.request.urlopen('http://httpbin.org/post', data=data)
    print(response.read())


def urllib_request_urlopen_timeout_test(timeout):
    # 设置请求的超时时间，该测试网站设置1s可行，0.1s会报错。
    try:
        response = urllib.request.urlopen('http://httpbin.org/get', timeout=timeout)
        print(response.read())
    except urllib.error.URLError as e:
        if isinstance(e.reason, socket.timeout):  # 判断错误类型是否是超时
            print('TIME OUT')


# urlopen 的响应内容：类型
def urlopen_response_type_test():
    # 返回的response是"http.client.HTTPResponse"类型
    response = urllib.request.urlopen('https://www.python.org')
    print(type(response))


# ————————————————————利用request.Request添加header——————————————————————　#
#
# 网站为了防止爬虫频繁访问造成网站瘫痪，会需要携带一些headers头部信息才能访问
#
def urllib_request_urlopen_header_ver1_test():
    # 使用Request的默认方法header
    request = urllib.request.Request('https://python.org')
    response = urllib.request.urlopen(request)
    print(response.read().decode('utf-8'))


def urllib_request_urlopen_header_ver2_test():
    # 自定义header的方法
    url = 'http://httpbin.org/post'
    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
        'Host': 'httpbin.org'
    }
    encode_dict = {
        'name': 'zhaofan'
    }
    # 第一步先打包post内容
    data = bytes(urllib.parse.urlencode(encode_dict), encoding='utf8')
    # 第二步用Request方法,把url,data,headers一起打包，指定方法是'POST'
    req_dic = urllib.request.Request(url=url, data=data, headers=headers, method='POST')
    response = urllib.request.urlopen(req_dic)
    print(response.read().decode('utf-8'))


def urllib_request_urlopen_header_ver3_test():
    # 自定义header的另一种方法
    url = 'http://httpbin.org/post'
    encode_dict = {
        'name': 'Germey'
    }
    # 第一步还是先打包post数据
    data = bytes(urllib.parse.urlencode(encode_dict), encoding='utf8')
    # 第二步可以先打包其他内容，再用add_header方法增加header,但是一次只能添加一组参数
    req_dic = urllib.request.Request(url=url, data=data, method='POST')
    req_dic.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')
    req_dic.add_header('Host', 'httpbin.org')
    response = urllib.request.urlopen(req_dic)
    print(response.read().decode('utf-8'))


# 网站会检测某一段时间某个IP的访问次数，如果过多它会禁止你访问,所以需要通过设置代理来继续爬取数据
def urllib_request_build_opener_proxyheadler_test():
    # 第一步使用request.Proxyhandler方法添加代理地址（底下是我的本地代理）
    proxy_handler = urllib.request.ProxyHandler({
        'http': 'http://127.0.0.1:8087',
        'https': 'https://127.0.0.1:8087'
    })
    # 第二步生成一个request.bulid_opener的实例代替原先的urlopen方法
    opener = urllib.request.build_opener(proxy_handler)
    # 第三步调用实例的open方法，这个方法使用起来和urlopen完全相同，接受Request打包的header
    response = opener.open('http://httpbin.org/get')
    print(response.read())


# 有时候爬取网站需要携带cookie信息访问
def urllib_request_HTTPCookieProcessor_test():
    # 先建一个CookieJar的实例，这个类包含了大部分关于cookie的操作
    cookie = http.cookiejar.CookieJar()
    # 使用实例初始化HTTPCookieProcessor类，这是个Header的派生类
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    response = opener.open('http://www.baidu.com')
    # print(response.read())
    for item in cookie:  # 我们没对cookie做任何操作，只有一些默认值
        print(item.name + "=" + item.value)


# cookie可以在本地存储读取
def urllib_request_HTTPCookieProcessor_file_ver1_test():
    # 方案一：使用http.cookiejar.MozillaCookieJar()方式
    filename = "cookie_Mozilla.txt"
    # 建一个MozillaCookieJar的实例,这是CookieJar的派生
    cookie = http.cookiejar.MozillaCookieJar(filename)
    # 首先当然可以从文件读取
    cookie.load('cookie_Mozilla.txt', ignore_discard=True, ignore_expires=True)
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    response = opener.open('http://www.baidu.com')
    # MozillaCookieJar包含save方法 (ignore_discard 忽略放弃, ignore_expires 忽略到期)
    cookie.save(ignore_discard=True, ignore_expires=True)


def urllib_request_HTTPCookieProcessor_file_ver2_test():
    # 方案二：使用http.cookiejar.LWPCookieJar()方式，过程差不多
    filename = 'cookie_LWP.txt'
    cookie = http.cookiejar.LWPCookieJar(filename)
    cookie.load('cookie_LWP.txt', ignore_discard=True, ignore_expires=True)
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    response = opener.open('http://www.baidu.com')
    cookie.save(ignore_discard=True, ignore_expires=True)


# ————————————————————异常处理,URLError———————————————————— #
#
def urllib_error_URLError_reason_test():
    # 尝试访问一个不存在的网页
    try:
        urllib.response = urllib.request.urlopen("http://pythonsite.com/1111.html")
    except urllib.error.URLError as e:
        print(e.reason)


# HTTPError是URLError的子类
# URLError里只有一个属性：reason, 即抓异常的时候只能打印错误信息
# HTTPError里有三个属性：code, reason, headers
def urllib_error_HTTPError_detail_test():
    try:
        urllib.response = urllib.request.urlopen("http://pythonsite.com/1111.html")
    except urllib.error.HTTPError as e:
        print("Http-reason:{0}\n".format(e.reason))
        print("Http-code:{0}\n".format(e.code))
        print("Http-headers:{0}\n".format(e.headers))
    except urllib.error.URLError as e:
        print("URL-reason:{0}\n".format(e.reason))

    else:
        print("reqeust successfully")


# e还可以进一步判断类型，作日志分析
def urllib_error_e_type_test():
    try:
        urllib.response = urllib.request.urlopen("http://www.pythonsite.com/", timeout=0.001)
    except urllib.error.URLError as e:
        print(type(e.reason))
        if isinstance(e.reason, socket.timeout):  # 判断是否是超时类型
            print("time out")


# ————————————————————urllib.parse模块，主要处理URL的解析————————————————————　#
#
# 分拆输入的网址：urllib.parse.urlparse(urlstring, scheme='', allow_fragments(允许分拆)=True)
# 结果：scheme='http', netloc='www.baidu.com', path='/index.html', params='user', query='id=5', fragment='comment'
def urllib_parse_urlparse_test():
    # result = urllib.parse.urlparse("http://www.baidu.com/index.html;user?id=5#comment")
    # 可以指定协议类型
    result = urllib.parse.urlparse("www.baidu.com/index.html;user?id=5#comment", scheme="https")
    print(result)


# 拼接输入的参数成网址：urllib.parse.urlunpars　这个拼接有逻辑关系
# 结果：http://www.baidu.com/index.html;user?a=123#commit
def urllib_parse_urlunpars_test():
    data = ['http', 'www.baidu.com', 'index.html', 'user', 'a=123', 'commit']
    print(urllib.parse.urlunparse(data))


# 另一个拼接用的方法：urllib.parse.urljoin 这个接拼直观很多，出现多个网址时使用最后一个
def urllib_parse_urljoin_test():
    print(urllib.parse.urljoin('http://www.baidu.com', 'FAQ.html'))
    print(urllib.parse.urljoin('http://www.baidu.com', 'https://pythonsite.com/FAQ.html'))
    print(urllib.parse.urljoin('http://www.baidu.com/about.html', 'https://pythonsite.com/FAQ.html'))
    print(urllib.parse.urljoin('http://www.baidu.com/about.html', 'https://pythonsite.com/FAQ.html?question=2'))
    print(urllib.parse.urljoin('http://www.baidu.com?wd=abc', 'https://pythonsite.com/index.php'))
    print(urllib.parse.urljoin('http://www.baidu.com', '?category=2#comment'))
    print(urllib.parse.urljoin('www.baidu.com', '?category=2#comment'))
    print(urllib.parse.urljoin('www.baidu.com#comment', '?category=2'))


# 第三个拼接方法，把字典转换为url参数：urllib.parse_urlencode
# 结果：http://www.baidu.com?age=23&name=zhaofan
def urllib_parse_urlencode_test():
    params = {
        "name": "zhaofan",
        "age": 23,
    }
    base_url = "http://www.baidu.com?"

    url = base_url + urllib.parse.urlencode(params)
    print(url)


if __name__ == "__main__":
    # urllib_request_urlopen_get_test()
    # urllib_request_urlopen_post_test()
    # urllib_request_urlopen_timeout_test(1)

    # urlopen_response_type_test()

    # urllib_request_urlopen_header_ver1_test()
    # urllib_request_urlopen_header_ver2_test()
    # urllib_request_urlopen_header_ver3_test()

    # urllib_request_build_opener_proxyheadler_test()
    # urllib_request_HTTPCookieProcessor_test()
    # urllib_request_HTTPCookieProcessor_file_ver1_test()
    # urllib_request_HTTPCookieProcessor_file_ver2_test()

    # urllib_error_URLError_reason_test()
    # urllib_error_HTTPError_detail_test()
    # urllib_error_e_type_test()

    # urllib_parse_urlparse_test()
    # urllib_parse_urlunpars_test()
    # urllib_parse_urljoin_test()
    urllib_parse_urlencode_test()
