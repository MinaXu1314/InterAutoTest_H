from config.Conf import ConfigYaml
import os
from common.ExcelData import Data
from utils.LogUtil import my_log
from common import ExcelConfig
from utils.RequestsUtil import Request
import json
import pytest
from common.Base import json_parse
import re

# 1.初始化信息
# 1).初始化测试用例文件
case_file = os.path.join("../data", ConfigYaml().get_excel_file())
# 2).初始化测试用例sheet名称
sheet_name = ConfigYaml().get_excel_sheet()
# 3).获取运行的测试用例列表
data_init = Data(case_file, sheet_name)
run_list = data_init.get_run_data()
# print(run_list)

# 4).初始化日志信息
log = my_log()
# 初始化DataConfig
data_key = ExcelConfig.DataConfig


# 2.编写测试用例方法，实现参数化运行
# 先完成一个测试用例的运行
class TestExcel:
    # 1. 增加Pytest参数化
    # 2. 修改方法参数
    # 3. 重构函数内容
    # 4. 通过pytest.main运行

    def run_api(self, url, method, params=None, header=None, cookie=None):
        """
        发送请求api
        :return: 
        """
        # 2).根据url发送接口请求
        request = Request()
        # params 获取的是字符类型  需要转义成json
        # 验证params有没有内容
        if len(str(params).strip()) is not 0:
            params = json.loads(params)
        # method: post / get
        if str(method).lower() == "get":
            # 2.增加headers
            res = request.get(url, json=params, headers=header, cookies=cookie)  # 4.增加cookies
        elif str(method).lower() == "post":
            res = request.post(url, json=params, headers=header, cookies=cookie)
        else:
            log.error("错误请求method：%s" % method)
        return res

    def run_pre(self, pre_case):
        url = ConfigYaml().get_conf_url() + pre_case[data_key.url]
        method = pre_case[data_key.method]
        params = pre_case[data_key.params]
        headers = pre_case[data_key.headers]
        cookies = pre_case[data_key.cookies]
        # 1.判断headers是否存在，存在：json转义  不存在：无需作任何操作
        # if headers:
        #     header = json.loads(headers)
        # else:
        #     header = headers
        header = json_parse(headers)
        # 3.判断cookies是否存在，存在：json转义  不存在：无需作任何操作
        # if cookies:
        #     cookie = json.loads(cookies)
        # else:
        #     cookie = cookies
        cookie = json_parse(headers)
        res = self.run_api(url, method, params, header)
        print(res)

    # 1).初始化信息：url、data
    # 1. 增加Pytest参数化
    @pytest.mark.parametrize("case", run_list)
    # 2. 修改方法参数
    def test_run(self, case):
        # 3. 重构函数内容
        # data_key = ExcelConfig.DataConfig
        # run_list第一个用例，根据key获取values
        url = ConfigYaml().get_conf_url() + case[data_key.url]
        print(url)
        case_id = case[data_key.case_id]
        case_model = case[data_key.case_model]
        case_name = case[data_key.case_name]
        pre_exec = case[data_key.pre_exec]
        method = case[data_key.method]
        params_type = case[data_key.params_type]
        params = case[data_key.params]
        expect_result = case[data_key.expect_result]
        headers = case[data_key.headers]
        cookies = case[data_key.cookies]
        status_code = case[data_key.status_code]
        db_verify = case[data_key.db_verify]

        # 1.判断headers是否存在，存在：json转义  不存在：无需作任何操作
        if headers:
            header = json.loads(headers)
        else:
            header = headers
        # 3.判断cookies是否存在，存在：json转义  不存在：无需作任何操作
        if cookies:
            cookie = json.loads(cookies)
        else:
            cookie = cookies

        # 1.验证前置条件是否存在
        if pre_exec:
            # 2.根据前置条件找到前置用例
            pre_case = data_init.get_case_pre(pre_exec)
            print("前置条件信息为：%s" % pre_case)
            self.run_pre(pre_case)

        # 2).根据url发送接口请求
        request = Request()
        # params 获取的是字符类型  需要转义成json
        # 验证params有没有内容
        if len(str(params).strip()) is not 0:
            params = json.loads(params)
        # method: post / get
        if str(method).lower() == "get":
            # 2.增加headers
            res = request.get(url, json=params, headers=header, cookies=cookie)  # 4.增加cookies
        elif str(method).lower() == "post":
            res = request.post(url, json=params, headers=header, cookies=cookie)
        else:
            log.error("错误请求method：%s" % method)
        print(res)


# TestExcel().test_run()

if __name__ == '__main__':
    # pytest.main(["-s", "test_excel_case_v6.py"])
    # 固定headers请求
    # 1.判断headers是否存在，存在：json转义  不存在：无需作任何操作
    # 2.增加Headers
    # 3.判断cookies是否存在，存在：json转义  不存在：无需作任何操作
    # 4.增加cookies
    # 5.发送请求

    # 动态关联
    # 1.验证前置条件是否存在
    # 2.根据前置条件找到执行用例
    # 3.发送请求，获取前置用例结果
    # 发送获取的前置测试用例，再获取它的用例结果
    # 4.替换Headers变量
        # 1.验证请求中是否含有${}$，如果有则返回${}内容
    str1 = '{"Authorization": "JWT ${token}$"}'
    if "${" in str1:
        print(str1)
    pattern = re.compile('\${(.*)}\$')
    re_res = pattern.findall(str1)
    # print(re_res)
    print(re_res[0])
        # 2.根据内容，查询 前置条件测试用例返回结果，进行赋值
    token = "123"
        # 3.获取到前置执行的结果，进行替换
    res = re.sub(pattern,token,str1)
    # print(res)
    # 5.发送请求验证结果

    """
    关联思路：
    1. 查询，做成公共方法
    2. 替换，做成公共方法
    3. 验证请求中是否含有${}$，如果有则返回${}内容，也做成公共方法
    4. 关联方法
    """

