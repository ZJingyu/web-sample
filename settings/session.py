import random
# 这个函数用来保存所有的 messages
# session持久化的两种方式：一种是保存成文件，另一种是对称加密
# session共享:QQ、微信、TCP等各程序间的session共享
message_list = []
session = {
    'session id': {
        'username': 'username',
        '过期时间': "2025-01-01: 00:00:00",
    }
}


def random_str():
    """
    生成一个随机的字符串
    """
    seed = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    s = ''
    for i in range(16):
        random_index = random.randint(0, len(seed) - 2)
        s += seed[random_index]
    return s


def current_user(request):
    session_id = request.cookies.get('user', '')
    username = session.get(session_id, '游客')
    return username
