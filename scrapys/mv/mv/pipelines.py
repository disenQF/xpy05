# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_DIR = os.path.join(BASE_DIR, 'images')


class MvPipeline(object):
    def process_item(self, item, spider):
        return item

class MvImgPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        # 获取item中的图片地址，并发起Request()请求
        for url in item['image_urls']:
            yield Request(url, meta={'name': item['name']})

    def item_completed(self, results, item, info):
        print(results)
        # 获取一个item中所有图片下载后的文件存放路径
        file_images = [x['path'] for ok, x in results if ok]
        if not file_images:
            raise Exception('当前的item不包含image_urls')

        item['images'] = file_images
        return item

    def file_path(self, request, response=None, info=None):
        name = request.meta.get('name')  # 获取主人公的姓名

        # 获取下载图片的文件名
        image_file_name = request.url.split('/')[-1]

        dir_ = os.path.join(IMAGE_DIR, name)
        if not os.path.exists(dir_):
            os.mkdir(dir_)

        # 返回的是相对于 IMAGES_STORE的文件路径
        # name/aaa.jpg
        return '%s/%s' % (name, image_file_name)
