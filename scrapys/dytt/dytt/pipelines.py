# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class DyttPipeline(object):
    def __init__(self):
        pass

    def filter_str(self, txt):
        return txt.replace(u'\u3000', '')

    def process_item(self, item, spider):
        # item是一个字典
        print(type(item))
        print('------>', item.get('name'))

        # 如果不返回item, engine引擎打印 None
        # 表示，如果存在其它的pipeline管道，则不会进入pipeline管道
        # 如果返回item,则其它的pipeline管道可以继续处理

    def __del__(self):
        pass
