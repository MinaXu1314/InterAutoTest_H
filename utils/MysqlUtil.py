import pymysql
from utils.LogUtil import my_log
"""
PyMysql工具类封装
1.创建封装类
2.初始化数据，连接数据库，创建光标对象
3.创建查询、执行方法
4.关闭对象
"""
class Mysql:  # 创建封装类
    # 初始化数据：连接数据库
    def __init__(self,host,user,password,database,charset="utf8",port=3306):
        self.conn = pymysql.connect(
            host = host,
            user = user,
            password = password,
            database = database,
            charset = charset,
            port = port  # mysql默认端口号3306
            )
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)  # 创建光标对象  返回字典
        self.log = my_log("mysql")
    # 创建查询、执行方法
    def fetchone(self, sql):
        """查询单个"""
        self.cursor.execute(sql)
        return self.cursor.fetchone()
    def fetchall(self, sql):
        """查询多个"""
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    # 创建执行方法
    def exec(self, sql):
        """执行：更新等操作"""
        try:
            if self.conn and self.cursor:
                self.cursor.execute(sql)
                self.conn.commit()
        except Exception as error:
            self.conn.rollback()
            self.log.error("Mysql 执行失败：%s" % error)
            return False
        return True
    # 关闭对象
    def __del__(self):
        # 关闭连接对象
        if self.conn is not None:
            self.conn.close()
        if self.cursor is not None:
            self.cursor.close()

if __name__ == '__main__':
    mysql = Mysql(
        host="211.103.136.242",
        user="test",
        password="test123456",
        database="meiduo",
        port=7090)
    # res = mysql.fetchone("select username, password from tb_users")
    # res = mysql.fetchall("select username, password from tb_users")
    res = mysql.exec("update tb_users set first_name = 'haha' where username = 'python' ")
    print(res)

"""
将数据库固定的信息提取出来，放到配置文件
1. 单独创建db_conf.yml(加入数据库有多个，如db1、db2等，如果放到之前的配置文件当中，会显得比较乱)
2. 编写数据库基本信息
3. 重构Conf.py
4. 执行
"""
