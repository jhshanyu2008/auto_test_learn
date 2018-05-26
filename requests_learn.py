"""
学习资料来源：http://www.cnblogs.com/zhaof/p/6915127.html
博客作者：python修行路
"""
import requests  # request库,本质是高度集成的urllib库
import json  # 用于解析json文本


# 主体功能的一个简单演示，request库比urllib要简洁不少
def request_brief_demonstration():
    response = requests.get("https://www.baidu.com")
    print(type(response))
    print(response.status_code)
    print(type(response.text))
    # 很多情况下的网站如果直接response.text会出现乱码的问题
    print(response.text)
    print(response.cookies)
    # 返回的数据格式其实是二进制格式，可以通过decode()转换为utf-8格式解决
    print(response.content)
    print(response.content.decode("utf-8"))


# 我们当然也可以指定页面编码（前提你知道），这样直接使用response.text也不会有乱码
def request_get_text_specified_encoding():
    response = requests.get("http://www.baidu.com")
    response.encoding = "utf-8"
    print(response.text)


# ————————————————————request的各种请求方式———————————————————— #
#
# 基本的get请求
def request_get_fundamental():
    response = requests.get('http://httpbin.org/get')
    response.encoding = "utf-8"
    print(response.text)


# 带参数的get请求，第一种方法可以直接写进url里
def request_get_with_paras_ver1():
    # 如果我们试图查询的话，我们一般会通过httpbin.org/get?key1=val1&key2=val2...方式传递给网站
    response = requests.get("http://httpbin.org/get?name=zhaofan&age=23")
    print(response.text)


# 带参数的get请求，第二种方法是打包成字典作为get的参数
def request_get_with_paras_ver2():
    data = {
        "name": "zhaofan",
        "age": 22
    }
    response = requests.get("http://httpbin.org/get", params=data)
    print(response.url)
    print(response.text)


# request.get也可以直接解析json文本
def request_get_explain_json():
    response = requests.get("http://httpbin.org/get")
    print(type(response.text))
    # 以下两条命令结果完全一样，可见get(url).json()调用的就是json.loads()命令
    print(response.json())
    print(json.loads(response.text))
    print(type(response.json()))


if __name__ == "__main__":
    # request_brief_demonstration()
    # request_get_text_specified_encoding()

    # request_get_fundamental()
    # request_get_with_paras_ver1()
    # request_get_with_paras_ver2()
    request_get_explain_json()
