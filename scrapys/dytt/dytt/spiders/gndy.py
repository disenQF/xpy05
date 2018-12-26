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

        # 下一页数据
        if next_a:
            yield Request(next_a)

    def parse_info(self, response):
        data = {}
        texts = response.css('#Zoom p::text').extract()
        if texts:
            # 处理数据，提取各个特征字段
            data['name'] = texts[0]
            data['zh_name'] = texts[2]
            data['en_name'] = texts[3]
            data['year'] = texts[4]
            data['location'] = texts[5]
            data['lb'] = texts[6]

            data['imgs'] = response.css('#Zoom img::attr(src)').extract()
            # 处理图片数据，第一个是海报， 第二个电影情节截图

            # 视频的下载地址
            data['video_ftp'] = response.xpath('//td[@style="WORD-WRAP: break-word"]/a/text()').extract()[0]

            return data

