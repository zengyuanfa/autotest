import cx_Oracle  # 导入Oracle连接库

class OracleTool:
    def __init__(self, user, password, host, port, service):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.service = service

    # 连接数据库
    def connect(self):
        dsn = cx_Oracle.makedsn(self.host, self.port, service_name=self.service)
        self.connection = cx_Oracle.connect(self.user, self.password, dsn)

    # 执行查询，并返回结果集
    def execute_query(self, sql):
        cursor = self.connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result

    # 执行插入、更新和删除操作
    def execute_update(self, sql):
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()

    # 关闭数据库连接
    def close(self):
        self.connection.close()

if __name__ == "__main__":
    # 实例化工具类
    oracle_tool = OracleTool('user', 'password', 'host', 'port', 'service')

    # 连接数据库
    oracle_tool.connect()

    # 查询数据
    result = oracle_tool.execute_query('select * from table')

    # 插入、更新、删除数据
    oracle_tool.execute_update('insert into table (col1, col2) values ("value1", "value2")')

    # 关闭数据库连接
    oracle_tool.close()