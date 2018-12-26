from unittest import TestCase   # 单元测试类

from dao.db import DB
from dao.base import BaseDao
from models.dytt import Dytt

class DBTestCase(TestCase):

    def test_1(self):
        self.assertIs(1, 1, 'python解释器的问题')

    def test_conn(self):
        db = DB(db='dytt')
        with db:
            # 断言db.conn不是None
            # 如果断言失败，表示db.conn是None,数据库连接失败!
            self.assertIsNotNone(db.conn, '数据库连接失败！')

            dao = BaseDao(db)
            data = Dytt('a', 'b', 'c', 2014, 'ftp://www.aa.cn/aa.mp4')
            dao.save(data)

