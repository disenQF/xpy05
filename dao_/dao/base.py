from datetime import time, datetime

from pymysql.cursors import Cursor


class BaseDao():
    def __init__(self, db):
        self.db = db

    def query(self, cls):
        # select * from 表名
        pass

    def query_by_id(self, cls, id):
        pass

    def __exist_table(self, table_name):
        cursor: Cursor = self.db.conn.cursor()
        cursor.execute('show tables')

        for table in cursor.fetchall():
            if table_name in table:
                return True  # False 表示不存在， True是存在

        print(f'---不存在 {table_name} 表----')
        return False

    def __create_table(self, table_name, field_names, field_values):
        cursor: Cursor = self.db.conn.cursor()
        sql = 'create table %s (%s)'  # name varchar
        fields = ''
        for index, field_name in enumerate(field_names):
            fields += '%s %s,' %(field_name,
                                 self.__get_db_type(field_values[index-1]))
        print(sql % (table_name,  fields[:-1]))


    def __get_db_type(self, value):
        if isinstance(value, str):
            if len(value)>255:
                return 'text' # clob/blob
            return 'varchar(255)'
        elif isinstance(value, float):
            return 'float'
        elif isinstance(value, int) or isinstance(value, bool):
            return 'int'
        elif isinstance(value, datetime):
            return 'date'

    def save(self, obj):
        # 判断表是否存在
        sql = 'insert %s(%s) values (%s)'
        table_name = 't_' + obj.__class__.__name__.lower()
        all_attr = obj.__dict__

        columns = ''
        columns_ = ''
        columns_values = []
        for key, value in all_attr.items():
            columns += key + ','
            columns_ += '%s,'  # values中的占位符 %s
            columns_values.append(value)  # 真实的值

        columns = columns[:-1]
        columns_ = columns_[:-1]

        sql = sql % (table_name, columns, columns_)

        if not self.__exist_table(table_name):
            self.__create_table(table_name, columns, columns_values)

        # cursor.execute(sql, tuple(columns_values))
        print(sql, tuple(columns_values))

    def update(self, obj):
        pass

    def delete(self, obj):
        pass