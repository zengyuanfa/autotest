#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os.path

from tradingMonitorTest.utils.LinuxTool import LinuxConnection
from tradingMonitorTest.utils.ExeclTool import ExcelUtil
from tradingMonitorTest.utils.RedisTool import RedisUtil

from tradingMonitorTest.tradeRecord.SGPTradeRecord import SGPTradeRecord


class TestSGPTradeMonitor(object):  # 测试用例类名必须用Test开头
    def setup(self):
        print('setup执行初始化操作')
        self.linux_conn = LinuxConnection('host', 'root', 'password')
        self.linux_conn.connect()
        remote_path = '/home/files'
        parent_path = os.path.dirname(os.path.dirname(__file__))
        self.local_path = os.path.join(parent_path, 'download/').replace('\\', '/')
        self.linux_conn.download_dir(remote_path, self.local_path)
        # 创建redis连接
        self.redis_conn = RedisUtil('host', 6379, 0, 'Zyf#2021')
        # 更新redis中的数据
        sgp = SGPTradeRecord()
        sgp.set_redis_hk_order_count()

    def teardown(self):
        print('teardown执销毁操作')
        self.linux_conn.disconnect

    def test_hk_buy_order_count(self):  # 方法名与函数名必须要用test_开头

        excel_util = ExcelUtil(os.path.join(self.local_path, 'excel.xlsx'))
        hk_buy_count_actual = excel_util.read_cell('Sheet1', 3, 2)
        print('hk_buy_count_actual', hk_buy_count_actual)
        # 查询hk_buy_count_expect
        # sgp = SGPTradeRecord()
        # hk_buy_count_expect = sgp.select_hk_buy_order_count()
        sgp_hk_order_count_redis = self.redis_conn.get_dict('sgp_hk_order_count_key')
        hk_buy_count_expect = sgp_hk_order_count_redis.get('buy')
        print('hk_buy_count_expect:', hk_buy_count_expect)
        assert hk_buy_count_actual == hk_buy_count_expect

# if __name__ == '__main__':
#     pytest.main('TestMonitorRet.py', '--html=report.html')
