def static_handler(request):
    """
    静态资源的架加载
    """
    filename = request.GET.get('file', 'dog.gif')
    path = request.static_path + filename
    with open(path, 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n'
        img = header + f.read()
    return img
