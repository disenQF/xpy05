"""
实现数据库连接的管理器
"""
from pymysql import Connect

class DB:
    def __init__(self, **kwargs):
        # host, port ,user, pwd, db, charset
        self.host = kwargs.get('host', '127.0.0.1')
        self.port = kwargs.get('port', 3306)  # mysql
        self.username = kwargs.get('user', 'root')
        self.password = kwargs.get('pwd', 'root')
        self.db = kwargs.get('db', 'mysql')
        self.charset = kwargs.get('charset', 'utf8')

    def connect(self):
        # 从连接池中获取数据连接
        self.conn = Connect(host=self.host,
                            port=self.port,
                            user=self.username,
                            password=self.password,
                            db=self.db,
                            charset=self.charset)

    def close(self):
        self.conn.close()

    def __enter__(self):
        self.connect()  # 连接数据库

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()