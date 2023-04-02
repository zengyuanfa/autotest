import redis

from tradingMonitorTest.utils import MySQLTool
from tradingMonitorTest.utils import RedisTool
class SGPTradeRecord(object):
    # 获取数据库连接

    def get_db_connection(self):
        db_conn = MySQLTool.MySQLUtil('host', 3306, 'root', 'Zyf#2021', 'monitor')
        return db_conn
    # 获取redis连接

    def get_redis_connection(self):
        redis_conn = RedisTool.RedisUtil('host', 6379, 0, 'Zyf#2021')
        return redis_conn
    # 查询hk的买入订单数量

    def select_hk_buy_order_count(self):
        db_conn = self.get_db_connection()
        sql = 'SELECT HK_Order_Count FROM singapore_buy'
        hk_buy_order_count = db_conn.execute_query(sql)['HK_Order_Count']
        return hk_buy_order_count
    # 查询hk的卖出订单数量
    def select_hk_sell_order_count(self):
        db_conn = self.get_db_connection()
        sql = 'SELECT HK_Order_Count FROM singapore_sell'
        hk_sell_order_count = db_conn.execute_query(sql)['HK_Order_Count']
        return hk_sell_order_count
    # 计算hk订单的net buy
    def cal_hk_net_buy_order_count(self):
        return self.select_hk_buy_order_count() - self.select_hk_sell_order_count()

    def cal_hk_total_order_count(self):
        return self.select_hk_buy_order_count() + self.select_hk_sell_order_count()

    def set_redis_hk_order_count(self):
        sgp_hk_order_count = {}
        sgp_hk_order_count['buy'] = self.select_hk_buy_order_count()
        sgp_hk_order_count['sell'] = self.select_hk_sell_order_count()
        sgp_hk_order_count['net_buy'] = self.cal_hk_net_buy_order_count()
        sgp_hk_order_count['total'] = self.cal_hk_total_order_count()
        redis_conn = self.get_redis_connection()
        sgp_hk_order_count_redis = redis_conn.get_dict('sgp_hk_order_count_key')
        if sgp_hk_order_count_redis is not None:
            redis_conn.delete('sgp_hk_order_count_key')
        redis_conn.set_dict('sgp_hk_order_count_key', sgp_hk_order_count)



if __name__ == '__main__':
    sgp_trade_record = SGPTradeRecord()
    sgp_trade_record.set_redis_hk_order_count()
    redis_conn = sgp_trade_record.get_redis_connection()
    sgp_hk_order_count = redis_conn.get_dict('sgp_hk_order_count_key')
    print(sgp_hk_order_count)
