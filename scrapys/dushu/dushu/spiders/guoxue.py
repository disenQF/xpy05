# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class GuoxueSpider(CrawlSpider):
    name = 'guoxue'
    allowed_domains = ['www.dushu.com']
    start_urls = ['https://www.dushu.com/guoxue/1001.html']

    rules = (
        # follow : True表示 针对提取的link下载并解析之后，会继续提取相关的规则、
        #          False，则在解析之后，不再继续提取
        # Rule()可以不用设置callback, 表示只提取连接(parse)，不解析下载后的数据
        Rule(LinkExtractor(allow=r'/guoxue/\d+/'), callback='parse_item', follow=False),
        Rule(LinkExtractor(restrict_css='.pages'), follow=True),
        Rule(LinkExtractor(r'https://www.dushu.com/guoxue/\d+\.html'), follow=True)
    )

    def parse_item(self, response):
        # 解析 图书的详情页面
        i = {}
        try:
            i['title'] = response.css('.book-title').xpath('h1/text()').extract()[0]
            i['image'] = response.css('.pic').xpath('img/@src').extract()[0]
            i['author'] = ''.join(response.css('.book-details-left').xpath('.//tr[1]/td[2]//text()').extract())

            # 提取规则
            chapter_extractor = LinkExtractor(restrict_css='#ctl00_c1_volumes_ctl00_chapters')
            i['volumes'] = [(link.text, link.url)
                            for link in chapter_extractor.extract_links(response)]
        except:
            print('----提取数据异常---', response.url)

        return i
