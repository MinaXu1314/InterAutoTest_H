import yaml
import os
"""
1. 创建类
2. 初始化，判断文件是否存在
3. yaml读取
"""
class YamlReader:
    # 初始化  判断文件是否存在
    def __init__(self, yaml_file):
        if os.path.exists(yaml_file):
            self.yaml_file = yaml_file
        else:
            raise FileNotFoundError("yaml文件不存在")
        self.__data = None
        self.__data_all = None

    def data(self):
        """yaml读取单个文档"""
        # 第一次调用data,读取yaml文档，如果不是，直接返回之前保存的数据
        if not self.__data:
            with open(self.yaml_file, "rb") as f:
                self.__data = yaml.safe_load(f)
        return self.__data

    def data_all(self):
        """yaml读取多个文档"""
        # 第一次调用data_all,读取yaml文档，如果不是，直接返回之前保存的数据
        if not self.__data_all:
            with open(self.yaml_file, "r", encoding="utf-8") as f:
                self.__data_all = list(yaml.safe_load_all(f))
        return self.__data_all