import re


def render(request, name, *args):
    path = request.template_path + name
    header = response_with_headers(request.response_headers, code=200)
    with open(path, encoding="utf-8", mode='r') as f:
        response = header + '\r\n' + f.read()
    if args:
        for k, v in args[0].items():
            response = re.sub("\{\{\s*%s\s*\}\}" % k, v, response)
    return response.encode("utf-8")


def httpresponse(string):
    return string.encode("utf-8")


def redirect(url):
    """浏览器在收到302响应的时候，会自动在http header中寻找Location字段并获取对应的url,然后自动请求这个url"""
    header = {
        'Location': url
    }
    response = response_with_headers(header, 302) + '\r\n'
    return response.encode("utf-8")


def response_with_headers(head, code=200):
    header = 'HTTP/1.1 {} OK\r\n'.format(code)
    header += ''.join(['{}: {}\r\n'.format(k, v) for k, v in head.items()])
    return header
