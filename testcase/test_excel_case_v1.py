from config.Conf import ConfigYaml
import os
from common.ExcelData import Data
from utils.LogUtil import my_log
from common import ExcelConfig
from utils.RequestsUtil import Request
import json
import pytest
# 1.初始化信息
# 1).初始化测试用例文件
case_file = os.path.join("../data", ConfigYaml().get_excel_file())
print(case_file)
# 2).初始化测试用例sheet名称
sheet_name = ConfigYaml().get_excel_sheet()
# 3).获取运行的测试用例列表
data_init = Data(case_file, sheet_name)
run_list = data_init.get_run_data()

# 4).初始化日志信息
log = my_log()
# 2.编写测试用例方法，实现参数化运行
# 先完成一个测试用例的运行
class TestExcel:

# 1).初始化信息：url、data
    def test_run(self):
        data_key = ExcelConfig.DataConfig
        # run_list第一个用例，根据key获取values
        url = ConfigYaml().get_conf_url() + run_list[0][data_key.url]
        # print(url)
        case_id = run_list[0][data_key.case_id]
        case_model = run_list[0][data_key.case_model]
        case_name = run_list[0][data_key.case_name]
        pre_exec = run_list[0][data_key.pre_exec]
        method = run_list[0][data_key.method]
        params_type = run_list[0][data_key.params_type]
        params = run_list[0][data_key.params]
        expect_result = run_list[0][data_key.expect_result]
        headers = run_list[0][data_key.headers]
        cookies = run_list[0][data_key.cookies]
        status_code = run_list[0][data_key.status_code]
        db_verify = run_list[0][data_key.db_verify]

        # 2).根据url发送接口请求
        request = Request()
        # params 获取的是字符类型  需要转义成json
        # 验证params有没有内容
        if len(str(params).strip()) is not 0:
            params = json.loads(params)
        # method: post / get
        if str(method).lower() == "get":
            # 2.增加headers
            res = request.get(url, json=params)
        elif str(method).lower() == "post":
            res = request.post(url, json=params)
        else:
            log.error("错误请求method：%s" % method)
        print(res)

# TestExcel().test_run()