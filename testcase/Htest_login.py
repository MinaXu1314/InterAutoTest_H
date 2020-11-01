from config import Conf
import os
from utils.YamlUtil import YamlReader
import pytest
from config.Conf import ConfigYaml
from utils.RequestsUtil import Request
"""
1. 获取测试用例内容List
# 获取testlogin.yml文件路径
# 使用工具类来读取多个文档内容
2. 参数化执行测试用例
"""

# 获取testlogin.yml文件路径
test_file = os.path.join(Conf.get_data_path(), "testlogin.yml")
# print(test_file)
# 使用工具类来读取多个文档内容
data_list = YamlReader(test_file).data_all()
print(data_list)
# 参数化执行测试用例
@pytest.mark.parametrize("login", data_list)
def test_yaml(login):
    # 初始化url，data
    url = ConfigYaml().get_conf_url() + login["url"]
    # print("url: %s" % url)
    data = login["data"]
    print("data: %s" % data)
    # 发送post请求
    request = Request()
    res = request.post(url, json=data)
    # 输出结果
    print(res)

if __name__ == '__main__':
    # pytest.main(["-s", "Htest_login.py"])
    pass