"""
登录成功	/authorizations/		POST	
json	{"username":"python","password":"12345678"}
"""
# 1. 导入包
import requests
import pytest
import json
from utils.RequestsUtil import requests_get, requests_post, Request
from config.Conf import ConfigYaml
from utils.AssertUtil import AssertUtil
from common.Base import init_db
# 2. 定义登陆方法
def test_login():
    # 3. 定义测试数据
    url = ConfigYaml().get_conf_url() + "/authorizations/"
    # url = "http://211.103.136.242:8064/authorizations/"
    json_data = {"username": "python", "password": "12345678"}
    # 4. 发送post请求
    # r = requests.post(url, json=json_data)
    # 调用封装的post方法
    # res = requests_post(url, json=json_data)
    # 调用Requests重构的post方法
    request = Request()
    res = request.post(url, json=json_data)
    # 5. 输出结果
    # print(r.json())
    print(res)
    # 验证
    # 返回状态码
    code = res["code"]
    # assert code == 201
    AssertUtil().assert_code(code, 200)
    # 返回结果内容
    # body = json.dumps(res["body"])
    body = res["body"]
    # assert '"user_id": 1, "username": "python"' in body
    AssertUtil().assert_in_body(body, '"user_id": 1, "username": "python"')

    # 1.初始化数据库对象
    conn = init_db("db_1")
    # 2.查询结果
    res_db = conn.fetchone("select id, username from tb_users where username = 'python'")
    print("数据库查询结果", res_db)
    # 3. 验证结果
    user_id = body["user_id"]
    assert user_id == res_db["id"]


def test_info():
    """获取个人信息"""
    # 定义测试数据
    url = ConfigYaml().get_conf_url() + "/user/"
    # url = "http://211.103.136.242:8064/user/"
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJlbWFpbCI6Ijk1MjY3MzYzOEBxcS5jb20iLCJ1c2VybmFtZSI6InB5dGhvbiIsImV4cCI6MTYwMDUyNDI2OH0.LcQtZN02kykI8zvmxw6Y6BOksc3rmQ8EF3BNboLinC4"
    headers = {"Authorization": "JWT " + token}
    # 发送请求
    # r = requests.get(url, headers=headers)
    # 调用封装的get方法
    # res = requests_get(url, headers=headers)
    # 调用Requests重构的get方法
    request = Request()
    res = request.get(url, headers=headers)
    # 输出结果
    # print(r.json())
    # print(r.text)
    print(res)

"""
商品列表数据	商品列表数据正确	/categories/115/skus/		
get	json	" {
 ""page"":""1"",
 ""page_size"": ""10"",
 ""ordering"": ""create_time""
 }"
"""

def goods_list():
    """获取商品列表数据"""
    # 定义测试数据
    url = ConfigYaml().get_conf_url() + "/categories/115/skus/"
    # url = "http://211.103.136.242:8064/categories/115/skus/"
    json_data = {"page": "1", "page_size": "10", "ordering": "create_time"}
    # 发送请求
    # r = requests.get(url, json=json_data)
    res = requests_get(url, json=json_data)
    # 输出结果
    # print(r.json())
    print(res)

"""
添加购物车成功	/cart/	login_4	post	
json	{"sku_id": "3","count": "1", "selected": "true"}
"""

def cart():
    """添加到购物车"""
    # 定义测试数据
    url = ConfigYaml().get_conf_url() + "/cart/"
    # url = "http://211.103.136.242:8064/cart/"
    json_data = {"sku_id": "3","count": "1", "selected": "true"}
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJlbWFpbCI6Ijk1MjY3MzYzOEBxcS5jb20iLCJ1c2VybmFtZSI6InB5dGhvbiIsImV4cCI6MTYwMDUyNDI2OH0.LcQtZN02kykI8zvmxw6Y6BOksc3rmQ8EF3BNboLinC4"
    headers = {"Authorization": "JWT " + token}
    # 发送请求
    # r = requests.post(url, json=json_data, headers=headers)
    res = requests_post(url, json=json_data, headers=headers)
    # 输出结果
    # print(r.json())
    print(res)

"""
保存订单	/orders/	login_4	post	
json	{ "address":"1","pay_method":"1" }
"""

def order():
    """保存订单"""
    # 定义测试数据
    url = ConfigYaml().get_conf_url() + "/orders/"
    # url = "http://211.103.136.242:8064/orders/"
    json_data = {"address": "1","pay_method": "1"}
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJlbWFpbCI6Ijk1MjY3MzYzOEBxcS5jb20iLCJ1c2VybmFtZSI6InB5dGhvbiIsImV4cCI6MTYwMDUyNDI2OH0.LcQtZN02kykI8zvmxw6Y6BOksc3rmQ8EF3BNboLinC4"
    headers = {"Authorization": "JWT " + token}
    # 发送请求
    # r = requests.post(url, json=json_data, headers=headers)
    res = requests_post(url, json=json_data, headers=headers)
    # 输出结果
    # print(r.json())
    print(res)

if __name__ == "__main__":
    # test_login()
    # info()
    # goods_list()
    # cart()
    # order()

    # 1.根据pytest默认运行规则，调整py文件命名，函数命名
    # 2.pytest.main()运行，或者命令行直接pytest运行
    pytest.main(["-s"])
