# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisCrawlSpider


class MmSpider(RedisCrawlSpider):
    name = 'mm'

    # 从redis中获取redis_key中的任务
    # redis_key 在redis中是list类型
    redis_key = 'mm:urls'

    rules = (
        Rule(LinkExtractor(allow=r'http://www.meinv.hk/\?p=\d+'), callback='parse_mv', follow=True),
    )

    def parse_mv(self, response):
        title = response.xpath('//title/text()').extract()[0]
        index = title.find('美女网')

        print(response.url, '请求成功', title[:index])
