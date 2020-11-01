from config.Conf import ConfigYaml
from utils.MysqlUtil import Mysql
import json
import re
from utils.AssertUtil import AssertUtil
from utils.LogUtil import my_log
import subprocess
from utils.EmailUtil import SendEmail
"""
1. 初始化数据库信息， Base.py  int_db
2. 接口用例返回结果内容进行数据库断言的验证
"""

p_data = '\${(.*)}\$'
log = my_log()
# 定义方法 init_db
def init_db(db_alias):
    # 通过读取配置文件，初始化数据库信息
    db_info = ConfigYaml().get_db_conf_info(db_alias)
    host = db_info["db_host"]
    user = db_info["db_user"]
    password = db_info["db_password"]
    db_name = db_info["db_name"]
    charset = db_info["db_charset"]
    port = int(db_info["db_port"])
    # 初始化Mysql对象
    conn = Mysql(host,user,password,db_name,charset,port)
    print(conn)
    return conn

def assert_db(db_name, result, db_verify):
    """
    数据库结果验证
    :param db_name: 
    :param result: 
    :param db_verify: 
    :return: 
    """
    # 1.初始化数据库
    # sql = init_db("db_1")
    sql = init_db(db_name)
    # 2.查询sql，excel文件中定义好的
    db_res = sql.fetchone(db_verify)
    # print(db_res)
    log.debug("数据库查询结果：{}".format(str(db_res)))
    # 3.数据库的结果与接口返回的结果验证
    # 获取数据库结果的key
    verify_list = list(dict(db_res).keys())
    # 根据key获取数据库结果，以及 接口返回的结果
    for line in verify_list:
        # res_line = res["body"][line]
        res_line = result[line]
        res_db_line = dict(db_res)[line]
        # 进行验证
        AssertUtil().assert_body(res_line, res_db_line)

def json_parse(data):
    """
    格式化字符，转换json格式
    :param data: 
    :return: 
    """
    # if headers:
    #     header = json.loads(headers)
    # else:
    #     header = headers
    return json.loads(data) if data else data

def res_find(data, pattern_data=p_data):
    """
    正则查询
    :param data: 
    :param pattern_data: 
    :return: 
    """
    # pattern = re.compile('\${(.*)}\$')
    pattern = re.compile(pattern_data)
    re_res = pattern.findall(data)
    return re_res

def res_sub(data, replace, pattern_data=p_data):
    """
    关联替换
    :param data: 
    :param replace: 
    :param pattern_data: 
    :return: 
    """
    pattern = re.compile(pattern_data)
    re_res = pattern.findall(data)
    if re_res:
        return re.sub(pattern_data, replace, data)
    return re_res

# 验证请求中是否有需要依赖结果的
def params_find(headers, cookies):
    """
    验证请求中是否有${}$，需要进行结果关联
    :param headers: 
    :param cookies: 
    :return: 
    """
    if "${" in headers:
        headers = res_find(headers)
    if "${" in cookies:
        cookies = res_find(cookies)
    return headers, cookies

def allure_report(report_path, report_html):
    """
    生成allure测试报告
    :param report_path: 
    :param report_html: 
    :return: 
    """
    # 执行命令 allure generate
    allure_cmd = "allure generate %s -o %s --clean" %(report_path, report_html)
    # 调用subprocess.call
    log.info("报告地址：")
    try:
        subprocess.call(allure_cmd, shell=True)
    except:
        log.error("执行用例失败，请检查下测试环境相关配置")
        raise

def send_mail(report_html_path="",content="",title="测试"):
    """
    发送邮件
    :param report_html_path: 
    :param content: 
    :param title: 
    :return: 
    """
    email_info = ConfigYaml().get_email_info()
    smtp_addr = email_info["smtpserver"]
    username = email_info["username"]
    password = email_info["password"]
    recv = email_info["receiver"]
    email = SendEmail(
        smtp_addr=smtp_addr,
        username=username,
        password=password,
        recv=recv,
        title=title,
        content=content,
        file=report_html_path)
    email.send_mail()

if __name__ == '__main__':
    init_db("UAT")
    # print(res_find('{"Authorization": "JWT ${token}$"}'))
    # print(res_sub('{"Authorization": "JWT ${token}$"}', "123"))
