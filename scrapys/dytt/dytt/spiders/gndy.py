# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request


class GndySpider(scrapy.Spider):
    name = 'gndy'
    allowed_domains = ['www.dytt8.net']
    start_urls = ['https://www.dytt8.net/html/gndy/dyzz/index.html']

    def parse(self, response):
        # 找出下一页的href
        base_href = 'https://www.dytt8.net/html/gndy/dyzz/'
        next_a = base_href + response.css('.x').xpath('.//a/@href').extract()[-2]

        print(next_a)

        # response.css() 返回SelectorList->可迭代
        # SelectorList.xpath()  -> Selector(xpath, data)
        #             .css()
        # Selector.extract() 提取数据data
        links = [('https://www.dytt8.net'+ulink.xpath('@href').extract()[0],
                  ulink.xpath('text()').extract()[0])
                 for ulink in response.css('.ulink')]

        for link, title in links:
            yield Request(link,
                          callback=self.parse_info,
                          meta={'title': title})

    def parse_info(self,response):
        texts = response.css('#Zoom p::text').extract()
        # 处理数据，提取各个特征字段

        imgs = response.css('#Zoom img::attr(src)').extract()
        # 处理图片数据，第一个是海报， 第二个电影情节截图

        # 视频的下载地址
        video_ftp = response.xpath('//td[@style="WORD-WRAP: break-word"]/a/text()').extract()[0]


