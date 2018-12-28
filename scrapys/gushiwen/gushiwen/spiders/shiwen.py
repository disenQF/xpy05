# -*- coding: utf-8 -*-
from http.client import HTTPResponse

import requests
import scrapy
from requests import get
from requests.cookies import RequestsCookieJar
from scrapy import FormRequest, Request

from gushiwen import yundm


class ShiwenSpider(scrapy.Spider):
    name = 'shiwen'
    allowed_domains = ['www.gushiwen.org', 'so.gushiwen.org', 'ip.cn', 'ip.tool.chinaz.com']

    def start_requests(self):

        # yield 发起FormRequest  请求
        self.login_url = 'https://so.gushiwen.org/user/login.aspx?from='
        code_url = 'https://so.gushiwen.org/RandCode.ashx'

        # 请求验证码
        resp:requests.Response = get(code_url)
        code_file_name = 'code.png'

        """
        -cookies--> <RequestsCookieJar[
          <Cookie ASP.NET_SessionId=coify3hfb2nsgvpug1anfdca for so.gushiwen.org/>,
          <Cookie codeyzgswso=697778476451f7da for so.gushiwen.org/>,
          <Cookie sec_tc=AQAAADLb/2SjsQAA3/8OziosznQqcb6J for so.gushiwen.org/>
          ]>
        """
        cookies: RequestsCookieJar = resp.cookies

        form_cookies = {}
        for key, value in resp.cookies.items():
            form_cookies[key] = value

        # 将验证码的图片保存
        with open(code_file_name, 'wb') as f:
            f.write(resp.content)

        yumdm_ = yundm.YDMHttp()
        yumdm_.login()  # 登录
        # 云打码，解析验证码
        cid, result = yumdm_.decode(code_file_name, 1004, 30)
        print(cid, result)

        data = {
            'email': '610039018@qq.com',
            'pwd': 'disen8888',
            'code': result
        }

        # 登录后，会产生cookie相关的信息
        # 要求： scrapy开启cookie存储
        yield FormRequest(self.login_url,
                          formdata=data,
                          callback=self.parse_logined,
                          cookies=form_cookies)

    def parse_logined(self, response):
        if response.url.startswith(self.login_url):
            print('-------登录失败--------')
            print(response.text)
            return self.start_requests()
        else:
            print('-------登录成功--------')
            print(response.url)
            titles = response.xpath('//div[@class="cont"]/p[1]/a/b/text()').extract()
            print('我的收藏: ', titles)

        yield Request('http://ip.tool.chinaz.com', callback=self.parse_cz)
        yield Request('https://ip.cn', callback=self.parse_ip_cn)

    def parse_cz(self, response):
        proxy_ip = response.xpath('//dd[@class="fz24"]/text()').extract()
        print(response.url, '---代理的ip->', proxy_ip)
        print('设置的代理ip', response.meta['proxy'])
        print(response.headers)
        print(response.url, '---ua->', response.request.headers.get('User-Agent'))

    def parse_ip_cn(self, response):
        proxy_ip = response.xpath('//div[@class="well"]/p[1]/code/text()').extract()
        print(response.url, '---代理的ip->', proxy_ip)
        print(response.url, '---ua->', response.request.headers.get('User-Agent'))
