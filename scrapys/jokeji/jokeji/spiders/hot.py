# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.http import Response


class HotSpider(scrapy.Spider):
    name = 'hot'
    allowed_domains = ['www.jokeji.cn']
    start_urls = ['http://www.jokeji.cn/hot.asp?me_page=1']

    def parse(self, response: Response):  # response -> scrapy.http.Response
        print(type(response))  # scrapy.http.response.html.HtmlResponse
        if response.status == 200:
            print(response.url, '--请求成功---')
            a_list = response.xpath('//a[@class="main_14"]') # [<Selector>]
            for a in a_list:
                # xpath() -> Selector
                href = 'http://www.jokeji.cn' + a.xpath('@href').extract()[0]
                title = a.xpath('text()').extract()[0]

                # 发起新的请求(不会立即执行)
                #   1） -> 新的请求会经过核心引擎压入到任务队列中
                #   2） -> 由下载器从任务队列中获取请求任务，如果下载中间件不处理，则直接下载。
                yield Request(href, callback=self.parse_content,
                                    meta={'title':title})

    def parse_content(self, response: Response):
        if response.status == 200:
            contents = response.xpath('//*[@id="text110"]//font/text()').extract()
            title = response.meta.get('title')

            return {'title': title,
                    'contents': contents}