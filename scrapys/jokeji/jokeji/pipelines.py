# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class JokejiPipeline(object):
    def process_item(self, item, spider):
        # 处理数据 item -> dict
        return item
