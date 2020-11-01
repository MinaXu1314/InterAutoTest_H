from config.Conf import ConfigYaml
import os
from common.ExcelData import Data
from utils.LogUtil import my_log
from common import ExcelConfig
from utils.RequestsUtil import Request
import json
import pytest

"""
1. 增加Pytest参数化
2. 修改方法参数
3. 重构函数内容
4. 通过pytest.main运行
"""

# 1.初始化信息
# 1).初始化测试用例文件
case_file = os.path.join("../data", ConfigYaml().get_excel_file())
# 2).初始化测试用例sheet名称
sheet_name = ConfigYaml().get_excel_sheet()
# 3).获取运行的测试用例列表
data_init = Data(case_file, sheet_name)
run_list = data_init.get_run_data()
print(run_list)

# 4).初始化日志信息
log = my_log()
# 2.编写测试用例方法，实现参数化运行
# 先完成一个测试用例的运行
class TestExcel:
# 1).初始化信息：url、data
    # 1. 增加Pytest参数化
    @pytest.mark.parametrize("case", run_list)
    # 2. 修改方法参数
    def test_run(self, case):
        # 3. 重构函数内容
        data_key = ExcelConfig.DataConfig
        # run_list第一个用例，根据key获取values
        url = ConfigYaml().get_conf_url() + case[data_key.url]
        # print(url)
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

if __name__ == '__main__':
    pytest.main(["-s", "test_excel_case_v2.py"])