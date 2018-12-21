"""
实现数据库连接的管理器
"""

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
        pass

    def close(self):
        pass

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass