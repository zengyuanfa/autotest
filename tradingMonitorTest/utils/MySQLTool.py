import pymysql

class MySQLUtil:
    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database, cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.conn.cursor()

    def execute_query(self, query, args=None, one=True):
        self.cursor.execute(query, args)
        if one:
            return self.cursor.fetchone()
        else:
            return self.cursor.fetchall()

    def execute_update(self, query):
        self.cursor.execute(query)
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()

if __name__ == "__main__":
    # 实例化
    host = 'host'
    username = 'root'
    password = 'Zyf#2021'
    db = MySQLUtil(host, 3306, username, password, 'monitor')

    # 执行查询操作：
    results = db.execute_query('SELECT HK_Order_Count FROM singapore_buy', one=False)
    print(results[1]['HK_Order_Count'])

    # 执行更新操作：
    # db.execute_update('INSERT INTO table (id, name, age) VALUES (1, "Tom", 25)')

    #关闭连接：
    db.close()