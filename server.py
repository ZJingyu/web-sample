import socket
from request import Request
from settings import *


def run(host="", port=3001):
    with socket.socket() as s:
        log('start at', '{}:{}'.format(host, port))
        s.bind((host, port))
        request = Request()

        while True:
            s.listen(3)
            connection, address = s.accept()
            receive = connection.recv(1024)
            receive = receive.decode("utf-8")

            if len(receive.split()) < 2:
                continue

            request(receive)                   # 请求入口，调用call方法
            response = request.control()       # 请求的响应

            connection.sendall(response)
            connection.close()


if __name__ == '__main__':
    run()
