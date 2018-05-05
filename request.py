import urllib.parse
from control import *
from settings import *


class Request(object):
    def __init__(self):
        self.method = "GET"
        self.path = ""
        self.POST = {}
        self.headers = {}
        self.GET = {}
        self.cookies = {}

        self.static_path = STATIC_PATH + "/"
        self.template_path = TEMPLATES_PATH + "/"

        self.response_headers = {
            'Content-Type': 'text/html',
        }  # 响应的head

    def post(self, body):
        """form用于把body解析为一个字典并返回"""
        items = body.split("&")
        query = {}
        if len(items) > 1:
            for item in items:
                item = urllib.parse.unquote(item)  # 处理参数中带有特殊字符的这种情况
                k, v = item.split("=")
                query[k] = v
        return query

    def control(self):
        url_dict = views_handler()                # 路由映射
        response = url_dict.get(self.path, self.error)   # 将self传递给视图函数
        return response(self)

    def error(self, error=404):
        e = {
            404: b'HTTP/1.x 404 NotFound\r\n\r\n<h1>Page Not Found!</h1>'
        }
        return e.get(error, b"")

    def add_cookies(self, headers):
        """从headers中解析Cookie"""
        cookie = headers.get('Cookie', '')
        kvs = cookie.split('; ')
        cookies = {}
        for kv in kvs:
            if '=' in kv:
                k, v = kv.split('=')
                cookies[k] = v
        return cookies

    def add_headers(self, head):
        """解析head"""
        lines = head.split('\r\n')[1:]
        headers = {}
        for line in lines:
            k, v = line.split(': ', 1)
            headers[k] = v
        return headers

    def __call__(self, receive):
        """
        整个程序的入口，该方法从浏览器发送的http中解析所有的request数据
        :param receive: POST请求体，以&为分割标志的字符串
        :return: None
        """
        head, body = receive.split("\r\n\r\n", 1)[:2]
        method, path = receive.split(" ", 2)[:2]

        log(" ".join((method, path)))
        # log(receive)

        self.method = method                           # 解析请求方式
        self.path, self.GET = parse_path(path)         # 解析请求路径，从请求头中获取GET请求参数
        self.POST = self.post(body)                    # 从请求体中获取POST请求参数
        self.headers = self.add_headers(head)          # 将剩余的head字段解析成dict
        self.cookies = self.add_cookies(self.headers)  # 从headers中获取Cookie并解析成cookies

