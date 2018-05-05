from url import *
from settings import *


# 路径解析
def parse_path(path):
    ind = path.find("?")
    if ind == -1:
        path_parse = path
        query = {}
    else:
        path_parse, query_string = path.split("?", 1)
        items = query_string.split("&")
        query = {}
        for item in items:
            k, v = item.split("=")
            query[k] = v
    return path_parse, query


# 路由映射
def views_handler():
    """路由映射"""
    url_dict = {}
    for arg in urlpattern:
        url_dict[arg[0]] = arg[1]
    url_dict["/static"] = static_handler
    return url_dict
