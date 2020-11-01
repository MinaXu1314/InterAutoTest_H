from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
"""
邮件的封装
1. 数据初始化
2. 定义发送邮件的方法
"""

# 数据初始化：用户名、密码、邮件接收者、邮件标题、邮件内容、邮件附件
class SendEmail:
    def __init__(self, smtp_addr, username, password, recv,
                 title, content=None, file=None):
        self.smtp_addr = smtp_addr
        self.username = username
        self.password = password
        self.recv = recv
        self.title = title
        self.content = content
        self.file = file

    # 定义发送邮件方法
    def send_mail(self):
        # 初始化邮件信息  我们要处理邮件相关的主体内容，需要使用一个类MIMEMultipart
        msg = MIMEMultipart()
        msg.attach(MIMEText(self.content, _charset="utf-8"))  # 添加邮件正文  如果要发送字符串相关的信息 需要使用到另一个类
        msg["Subject"] = self.title
        msg["From"] = self.username
        msg["To"] = self.recv
        # 初始化邮箱附件
        # 1.判断是否有附件
        if self.file:
        # 2.使用MIMEText类读取文件
            att = MIMEText(open(self.file).read())
        # 3.设置内容类型
            att["Content-Type"] = 'application/octet-stream'
        # 4.设置附件头
            att["Content-Disposition"] = 'attachment;filename="%s"' % self.file
        # 5.将内容附加到邮件主体中
            msg.attach(att)
        # 登陆邮件服务器
        self.smtp = smtplib.SMTP_SSL(self.smtp_addr,port=465)
        self.smtp.login(self.username, self.password)
        # 发送邮件
        self.smtp.sendmail(self.username, self.recv, msg.as_string())

if __name__ == '__main__':
    # 初始化类  self, smtp_addr, username, password, recv,
    #              title, content, file)
    from config.Conf import ConfigYaml
    email_info = ConfigYaml().get_email_info()
    smtp_addr = email_info["smtpserver"]
    username = email_info["username"]
    password = email_info["password"]
    recv = email_info["receiver"]
    email = SendEmail(smtp_addr, username, password, recv, "测试")
    email.send_mail()
    # 封装公共方法
    # 应用到测试用例当中发送邮件