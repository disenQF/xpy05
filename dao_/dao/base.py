class BaseDao():
    def query(self, cls):
        pass

    def query_by_id(self, cls, id):
        pass

    def save(self, obj):
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

        # cursor.execute(sql, tuple(columns_values))
        print(sql)

    def update(self, obj):
        pass

    def delete(self, obj):
        pass