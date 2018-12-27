# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class GuoxueSpider(CrawlSpider):
    name = 'guoxue'
    allowed_domains = ['www.dushu.com']
    start_urls = ['https://www.dushu.com/guoxue/1001.html']

    rules = (
        Rule(LinkExtractor(allow=r'/guoxue/\d+/'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_css='.pages'), follow=True)
    )

    def parse_item(self, response):
        # 解析 图书的详情页面
        i = {}
        i['title'] = response.css('.book-title').xpath('h1/text()').extract()[0]
        i['image'] = response.css('.pic').xpath('img/@src').extract()[0]
        i['author'] = ''.join(response.css('.book-details-left').xpath('.//tr[1]/td[2]//text()').extract())

        # 提取规则
        chapter_extractor = LinkExtractor(restrict_css='#ctl00_c1_volumes_ctl00_chapters')
        i['volumes'] = [(link.text, link.url)
                        for link in chapter_extractor.extract_links(response)]

        return i
