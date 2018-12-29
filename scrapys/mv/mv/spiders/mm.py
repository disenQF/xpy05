# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisCrawlSpider

from mv.items import MvItem

class MmSpider(RedisCrawlSpider):
    name = 'mm'

    # 从redis中获取redis_key中的任务
    # redis_key 在redis中是list类型
    redis_key = 'mm:urls'

    rules = (
        Rule(LinkExtractor(allow=r'http://www.meinv.hk/\?p=\d+'), callback='parse_mv', follow=True),
    )

    def parse_mv(self, response):
        i = MvItem()
        i['name'] = response.xpath('//div[@class="post-title"]//h1[1]/text()').extract()[0]
        i['image_urls'] = response.css('.post-image').xpath('./img/@src').extract()
        i['info'] = response.css('.post-content').xpath('p/text()').extract()

        return i
