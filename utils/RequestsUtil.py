import requests
from utils.LogUtil import my_log
"""
get方法封装：
1. 创建封装get方法
2. 发送requests get请求
3. 获取结果相应内容
4. 内容存到字典
5. 字典返回
"""
# 1.创建封装get方法
def requests_get(url, json=None, headers=None):
    """get封装"""
    # 2.发送get请求
    r = requests.get(url, json=json, headers=headers)
    # 3. 获取结果相应内容
    code = r.status_code
    try:
        body = r.json()
    except Exception as error:
        body = r.text
    # 定义字典
    res = dict()
    # 响应内容存到字典
    res["code"] = code
    res["body"] = body
    # 返回字典
    return res

"""
post方法封装
1. 创建post封装方法
2. 发送post请求
3. 获取响应内容
4. 内容存到字典
5. 字典返回
"""
# 创建Post封装方法
def requests_post(url, data=None, json=None, headers=None):
    """post封装"""
    # 发送post请求
    r = requests.post(url, json=json, headers=headers)
    # 获取响应内容
    code = r.status_code
    try:
        body = r.json()
    except Exception as error:
        body = r.text
    # 定义空字典
    res = dict()
    # 响应内容存到字典
    res["code"] = code
    res["body"] = body
    # 返回字典
    return res
"""
requests重构
1. 创建类
2. 定义公共方法
3. 重构get/post方法
"""
# 1.创建类
class Request:
    # 2.定义公共方法
    def __init__(self):
        self.log = my_log("Requests")
    def request_api(self,url, data=None, json=None, headers=None, cookies=None, method="get"):
        # 判断get 还是 post
        if method == "get":
            # get请求
            self.log.debug("发送get请求")
            r = requests.get(url, data=data, json=json, headers=headers, cookies=cookies)
        elif method == "post":
            # post请求
            self.log.debug("发送post请求")
            r = requests.post(url, data=data, json=json, headers=headers, cookies=cookies)
        # 获取响应内容
        code = r.status_code
        try:
            body = r.json()
        except Exception as error:
            body = r.text
        # 定义空字典
        res = dict()
        # 响应内容存到字典
        res["code"] = code
        res["body"] = body
        # 返回字典
        return res

    def get(self,url, **kwargs):
        """重构get"""
        return self.request_api(url, method="get", **kwargs)

    def post(self,url, **kwargs):
        """重构post"""
        return self.request_api(url, method="post", **kwargs)