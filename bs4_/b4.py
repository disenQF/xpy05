"""
学习beautifulSoup的select选择器
古诗文-名句
https://so.gushiwen.org/mingju/
"""
import random
from urllib.request import Request, build_opener,ProxyHandler

import time
from bs4 import BeautifulSoup

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from bs4_.utils import decode_html


headers = {
    'User-Agent': 'BaiduSpider'
}

# 构造Browser
opener = build_opener(ProxyHandler(proxies={
    'http': '119.101.114.198:9999'
}))


def download(url, callback):
    try:
        resp = opener.open(Request(url, headers=headers))
        if resp.code == 200:
            print(f'请求 {url} ok!')
            callback(resp)
    except Exception as e:
        print(e)


def parse(resp):
    html = decode_html(resp.read(), resp.headers.get('Content-Type'))

    soup = BeautifulSoup(html, 'lxml')  # 通过bs4解析
    conts = soup.select('div[class=cont]')  # list
    for cont in conts:  # 每个元素都是Tag类型
        as_ = cont.select('a')  # list
        if len(as_) == 2:
            content_tag, author_title_tag = tuple(as_)  # Tag对象
            item_pipeline(content=content_tag.text,
                          author_title=author_title_tag.text)

    # 请求下一页数据
    more = soup.select('.amore')  # list
    if more:
        next_page_url = 'https://so.gushiwen.org'+more[0].get('href')
        print('准备读取下一页的数据')
        time.sleep(random.uniform(3, 5))
        download(next_page_url, parse)
    else:
        print('没有下一页了')


def item_pipeline(**data):
    print(data)


if __name__ == '__main__':
    download('https://so.gushiwen.org/mingju/',  parse)

