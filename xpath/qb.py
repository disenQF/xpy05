"""
爬取糗事百科的文本段子数据
数据包含： 用户名， 头像， 段子文本数据
"""
from http.client import HTTPResponse
from urllib.request import urlopen, Request
import csv
from lxml import etree

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

url = 'https://www.qiushibaike.com/text/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/71.0.3578.98 Safari/537.36'
}


def start_spider(url):
    # 过滤url是否为重复？
    resp = urlopen(Request(url, headers=headers))
    if resp.code == 200:
        print('请求', url, '成功')
        parse(resp)  # 解析
    else:
        # 尝试更改代理，重新下载？
        print('请求', url, '失败')


def parse(resp: HTTPResponse):
    try:
        html = resp.read().decode()
    except:
        # 如果网页编码不是utf-8或ISO8859-1，如gbk,gb2312
        # 在响应头中存在-> Content-Type: text/html; charset=UTF-8
        content_type = resp.headers.get('Content-Type')
        mime_type, charset = tuple(content_type.split(';'))
        print(mime_type, charset)
        if charset:
            html = resp.read().decode(encoding=charset)
        else:
            html = resp.read().decode(encoding='gbk')

    et = etree.HTML(html)

    # 通过xpath选择所有的段子 class = "article block untagged mb15 typs_long"
    article_divs = et.xpath('//div[starts-with(@class, "article")]')  # 默认情况选择48个Element(div)
    for article_div in article_divs:
        # 获取作者的信息
        author = article_div.xpath('./div[1]//img')  # Element->img
        if author:
            author_name = author[0].xpath('./@alt')[0]
            author_src = 'https:' + author[0].xpath('./@src')[0]

            # 获取段子文本数据
            text = article_div.xpath('./a[1]//span/text()')  # span内容可能包含<br>标签
            text = ''.join(text)

            item = {
                'author_name': author_name,
                'author_photo': author_src,
                'text': text
            }

            item_pipeline(**item)


def item_pipeline(**data):
    with open('qb.csv', 'a') as f:
        writer = csv.DictWriter(f, fieldnames=('author_name', 'author_photo', 'text'))
        writer.writerow(data)


def read_csv(filename):
    with open('qb.csv') as f:
        reader = csv.DictReader(f, fieldnames=('author_name', 'author_photo', 'text'))
        for row in reader:
            print(row.values())


if __name__ == '__main__':
    # start_spider(url)
    read_csv('qb.csv')
