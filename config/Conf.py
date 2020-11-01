import os
from utils.YamlUtil import YamlReader
# 1.获取项目基本目录
# 获取当前项目的的绝对路径
current = os.path.abspath(__file__)
# print(current)
BASE_DIR = os.path.dirname(os.path.dirname(current))
# print(BASE_DIR)
# print(os.path.dirname(os.getcwd()))
# 定义config目录的路径
_config_path = BASE_DIR + os.sep + "config"
# 定义conf.yml文件的路径
_config_file = _config_path + os.sep + "conf.yml"
# 定义db_conf.yml文件的路径
_db_config_file = _config_path + os.sep + "db_conf.yml"
# 定义logs目录路径
_log_path = BASE_DIR + os.sep + "logs"
# 定义data目录路径
_data_path = BASE_DIR + os.sep + "data"
# 定义report目录路径
_report_path = BASE_DIR + os.sep + "report"

def get_report_path():
    """
    获取report绝对路径
    :return: 
    """
    return _report_path

def get_config_path():
    return _config_path

def get_config_file():
    return _config_file

def get_db_conf_file():
    return _db_config_file

def get_log_path():
    """
    获取log文件路径
    :return: 
    """
    return _log_path

def get_data_path():
    """
    获取data目录路径
    :return: 
    """
    return _data_path

# 2.读取配置文件
class ConfigYaml:
    def __init__(self):
        self.config = YamlReader(get_config_file()).data()
        self.db_config = YamlReader(get_db_conf_file()).data()
    # 定义方法获取需要信息
    def get_conf_url(self):
        """获取url"""
        return self.config["BASE"]["test"]["url"]

    def get_excel_file(self):
        """
        获取测试用例excel名称
        :return: 
        """
        return self.config["BASE"]["test"]["case_file"]

    def get_excel_sheet(self):
        """
        获取测试用例sheet名称
        :return: 
        """
        return self.config["BASE"]["test"]["case_sheet"]

    def get_conf_log_level(self):
        """
        获取日志级别
        :return: 
        """
        return self.config["BASE"]["log_level"]

    def get_conf_log_extension(self):
        """
        获取日志文件的扩展名
        :return: 
        """
        return self.config["BASE"]["log_extension"]

    def get_db_conf_info(self, db_alias):
        """
        根据db_alias获取该名称下的数据库信息
        :param db_alias: 
        :return: 
        """
        return self.db_config[db_alias]

    def get_email_info(self):
        """
        获取邮箱配置相关信息
        :return: 
        """
        return self.config["email"]

if __name__ == "__main__":
    conf_read = ConfigYaml()
    # print(conf_read.get_conf_url())
    # print(conf_read.get_conf_log_level())
    # print(conf_read.get_conf_log_extension())
    # print(conf_read.get_db_conf_info("db_3"))
    # print(conf_read.get_excel_file())
    # print(conf_read.get_excel_sheet())
    print(conf_read.get_email_info())