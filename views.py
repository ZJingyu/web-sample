from settings import *
from models import *


def index(request):
    """返回主页响应"""
    return render(request, "index.html")


def login(request):
    """ 返回login界面"""
    username = current_user(request)  # 从cookie中获取用户名
    if request.method == "POST":
        name = request.POST.get("username")
        pwd = request.POST.get("password")
        if name == "alex" and pwd == "123":
            session_id = random_str()   # 生成随机字符串
            session[session_id] = name
            request.response_headers['Set-Cookie'] = 'user={}'.format(session_id)  # 用Set-Cookie告诉浏览器生成cookie
            result = "登录成功!"
        else:
            result = "用户名或密码错误!"
    else:
        result = ""
    return render(request, "login.html", {"result": result, "username": username})


def register(request):
    """用户注册界面"""
    if request.method == "POST":
        name = request.POST.get("username")
        pwd = request.POST.get("password")
        if len(name) > 2 and len(pwd) > 2:
            u = User.new({"username": name, "password": pwd})
            u.save()
            result = "注册成功<br> <pre>{}</pre>".format(User.all())
        else:
            result = '用户名或者密码长度必须大于2'
    else:
        result = ''
    return render(request, "register.html", {"result": result})


def message(request):
    """存储form表单里的数据"""
    username = current_user(request)  # 用cookie来实现登录验证
    if username == "游客":
        log("**debug 游客未登录")
        return redirect('/')
    log('本次请求的 method', request.method)
    if request.method == "POST":
        name = request.POST.get("username")
        pwd = request.POST.get("password")
        msg = Message.new({"username": name, "password": pwd})
        message_list.append(msg)
    return render(request, "html_basic.html", {"messages": '<br>'.join([str(m) for m in message_list])})


