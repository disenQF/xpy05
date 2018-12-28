# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from dytt.dao.db import DB
from dytt.dao.base import BaseDao
from dytt.models.dytt import Dytt

class DyttPipeline(object):
    def __init__(self):
        db = DB(db='dytt')
        db.connect()  # 连接数据库
        self.dao = BaseDao(db)

    def filter_str(self, txt):
        return txt.replace(u'\u3000', '')

    def process_item(self, item, spider):
        # item是一个字典
        print(type(item))
        print('------>', item.get('name'))

        # 如果不返回item, engine引擎打印 None
        # 表示，如果存在其它的pipeline管道，则不会进入pipeline管道
        # 如果返回item,则其它的pipeline管道可以继续处理
        dytt_obj = Dytt(name=item.get('name'),
                        zh_name=item.get('zh_name'),
                        en_name=item.get('en_name'),
                        year=item.get('year'),
                        video_ftp=item.get('video_ftp'))

        # 判断数据是否已存在
        if not self.dao.query_exist('t_dytt', 'where name=%s', (item.get('name'),)):
            self.dao.save(dytt_obj)
        else:
            print(f'{item.get("name")} 已存在')

        return item

    def __del__(self):
        self.dao.db.close()
