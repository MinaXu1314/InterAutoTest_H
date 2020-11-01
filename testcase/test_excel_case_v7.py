from config.Conf import ConfigYaml
from config import Conf
import os
from common.ExcelData import Data
from utils.LogUtil import my_log
from common import ExcelConfig
from utils.RequestsUtil import Request
import json
import pytest
from common.Base import json_parse
import re
from common import Base
from utils.AssertUtil import AssertUtil
from common.Base import init_db
import allure

# 1.初始化信息
# 1).初始化测试用例文件
case_file = os.path.join(Conf.get_data_path(), ConfigYaml().get_excel_file())
# 2).初始化测试用例sheet名称
sheet_name = ConfigYaml().get_excel_sheet()
# 3).获取运行的测试用例列表
data_init = Data(case_file, sheet_name)
run_list = data_init.get_run_data()
print(run_list)

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
        cookie = json_parse(cookies)
        res = self.run_api(url, method, params, header)
        print("前置用例执行：%s" % res)
        return res
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
        # if headers:
        #     header = json.loads(headers)
        # else:
        #     header = headers
        # header = json_parse(headers)
        # 3.判断cookies是否存在，存在：json转义  不存在：无需作任何操作
        # if cookies:
        #     cookie = json.loads(cookies)
        # else:
        #     cookie = cookies
        # cookie = json_parse(cookies)

        # 1.验证前置条件是否存在
        if pre_exec:
            # 2.根据前置条件找到前置用例
            pre_case = data_init.get_case_pre(pre_exec)
            print("前置条件信息为：%s" % pre_case)
            pre_res = self.run_pre(pre_case)
            headers, cookies = self.get_correlation(headers,cookies,pre_res)
        header = json_parse(headers)
        cookie = json_parse(cookies)
        res = self.run_api(url, method, params, header, cookie)
        print("测试用例执行：%s" % res)

        # 生成allure测试报告
        # sheet名称  feature 一级标签
        allure.dynamic.feature(sheet_name)
        # 模块   story 二级标签
        allure.dynamic.story(case_model)
        # 用例ID+接口名称  title
        allure.dynamic.title(case_id + case_name)
        # 请求URL  请求类型 期望结果 实际结果描述
        desc = "<font color='red'>请求url: </font>{}<Br/>" \
               "<font color='red'>请求类型：</font>{}<Br/>" \
               "<font color='red'>期望结果：</font>{}<Br/>" \
               "<font color='red'>实际结果：</font>{}".format(url, method, expect_result, res)
        allure.dynamic.description(desc)  # 执行allure命令


        #断言验证
        # 验证状态码
        AssertUtil().assert_code(int(res["code"]), int(status_code))
        # 验证返回结果内容
        AssertUtil().assert_in_body(str(res["body"]), str(expect_result))
        # 数据库结果断言
        Base.assert_db("db_1", res["body"], db_verify)
        # # 1.初始化数据库
        # sql = init_db("db_1")
        # # 2.查询sql，excel文件中定义好的
        # db_res = sql.fetchone(db_verify)
        # # print(db_res)
        # log.debug("数据库查询结果：{}".format(str(db_res)))
        # # 3.数据库的结果与接口返回的结果验证
        # # 获取数据库结果的key
        # verify_list = list(dict(db_res).keys())
        # # 根据key获取数据库结果，以及 接口返回的结果
        # for line in verify_list:
        #     res_line = res["body"][line]
        #     res_db_line = dict(db_res)[line]
        # # 进行验证
        #     AssertUtil().assert_body(res_line, res_db_line)
        # 2).根据url发送接口请求
        # request = Request()
        # # params 获取的是字符类型  需要转义成json
        # # 验证params有没有内容
        # if len(str(params).strip()) is not 0:
        #     params = json.loads(params)
        # # method: post / get
        # if str(method).lower() == "get":
        #     # 2.增加headers
        #     res = request.get(url, json=params, headers=header, cookies=cookie)  # 4.增加cookies
        # elif str(method).lower() == "post":
        #     res = request.post(url, json=params, headers=header, cookies=cookie)
        # else:
        #     log.error("错误请求method：%s" % method)
        # print(res)
        # res = self.run_api(url, method, params, header,cookie)
        # print("测试用例执行：%s" % res)


# TestExcel().test_run()

    def get_correlation(self, headers, cookies, pre_res):
        """
        关联替换
        :param headers: 
        :param cookies: 
        :param pre_res: 
        :return: 
        """
        # 验证是否有关联
        headers_para, cookies_para = Base.params_find(headers, cookies)
        # 若有关联，执行前置用例，获取结果
        if len(headers_para):
            headers_data = pre_res["body"][headers_para[0]]
        # 结果替换
            headers = Base.res_sub(headers, headers_data)
        if len(cookies_para):
            cookies_data = pre_res["body"][cookies_para[0]]
        # 结果替换
            cookies = Base.res_sub(cookies, cookies_data)
        return headers,cookies

if __name__ == '__main__':
    # pass
    report_path = Conf.get_report_path() + os.sep + "result"
    report_html_path = Conf.get_report_path() + os.sep + "html"
    pytest.main(["-s", "test_excel_case_v7.py", "--alluredir", report_path])
    # Base.allure_report(report_path, report_html_path)
    # Base.send_mail(title="接口测试报告结果",content=report_html_path)
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
    # str1 = '{"Authorization": "JWT ${token}$"}'
    # if "${" in str1:
    #     print(str1)
    # pattern = re.compile('\${(.*)}\$')
    # re_res = pattern.findall(str1)
    # print(re_res[0])
    #     # 2.根据内容，查询 前置条件测试用例返回结果，进行赋值
    # token = "123"
    #     # 3.获取到前置执行的结果，进行替换
    # res = re.sub(pattern,token,str1)
    # print(res)
    # # 5.发送请求验证结果

    # """
    # 关联思路：
    # 1. 查询，做成公共方法
    # 2. 替换，做成公共方法
    # 3. 验证请求中是否含有${}$，如果有则返回${}内容，也做成公共方法
    # 4. 关联方法
    # """

