import logging
import datetime
import os
from config.Conf import get_log_path,ConfigYaml

# 定义日志级别的映射
log_l = {
    "info": logging.INFO,
    "debug": logging.DEBUG,
    "warning": logging.WARNING,
    "error": logging.ERROR
}

# 创建工具类
# 1.创建类
class Logger:
# 2.定义参数
    # 输出文件名称、Loggername、日志级别
    def __init__(self, log_file, log_name, log_level):
        self.log_file = log_file  # logs包里的一个文件名称，文件名称不固定，可以取当前时间命名，但它的扩展名是固定的，扩展名可以放在配置文件
        self.log_name = log_name  # 传递参数，不用放在配置文件
        self.log_level = log_level  # 配置文件  可配置
# 3.编写输出控制台或文件
        # 设置logger名称
        self.logger = logging.getLogger(self.log_name)
        # 设置log级别
        self.logger.setLevel(log_l[self.log_level])
        # 判断handler是否存在
        if not self.logger.handlers:
            # 定义输出格式
            formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
            # 输出控制台
            fh_stream = logging.StreamHandler()
            fh_stream.setLevel(log_l[self.log_level])
            fh_stream.setFormatter(formatter)
            # 写入文件
            fh_file = logging.FileHandler(self.log_file)
            fh_file.setLevel(log_l[self.log_level])
            fh_file.setFormatter(formatter)
            # 添加handler
            self.logger.addHandler(fh_stream)  # 控制台
            self.logger.addHandler(fh_file)  # 文件

# 1.初始化参数数据：日志文件名称、日志文件级别
# 日志文件名称 = Logs目录 + 当前时间 + 扩展名
# 日志目录
log_path = get_log_path()
# 获取当前时间
current_time = datetime.datetime.now().strftime("%Y-%m-%d")
# 获取扩展名
log_extension = ConfigYaml().get_conf_log_extension()
# 拼接文件名
logfile = os.path.join(log_path, current_time+log_extension)
# print(logfile)
# 日志文件级别
log_level = ConfigYaml().get_conf_log_level()
# print(log_level)
# 2.定义对外提供的方法：初始化log工具类，提供给其他类使用
def my_log(log_name = __file__):
    return Logger(log_file=logfile, log_name=log_name, log_level=log_level).logger

if __name__ == "__main__":
    my_log().debug("this is a debug")