# -*- coding: utf-8 -*-
import scrapy


class ShiwenSpider(scrapy.Spider):
    name = 'shiwen'
    allowed_domains = ['www.gushiwen.org', 'so.gushiwen.org']
    start_urls = ['http://www.gushiwen.org/']

    def parse(self, response):
        pass
