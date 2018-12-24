"""
https://www.gushiwen.org/gushi/sanbai.aspx
基于beautifulSoupr爬取古诗文
"""
import re
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup, Tag

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from bs4_.utils import decode_html

url = 'https://www.gushiwen.org/gushi/sanbai.aspx'
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:64.0) Gecko/20100101 Firefox/64.0'

headers = {
    'User-Agent': user_agent
}


def download(url):
    try:
        resp = urlopen(Request(url, headers=headers))
        if resp.code == 200:
            print(f'request {url} ok')  # format格式字符串-> python 3.6+
            parse(resp)
        else:
            print(f'request {url} fail: {resp.code}')  # 20x
    except HTTPError as e:
        print(e)


def parse(resp):
    content_type = resp.headers.get('Content-Type')

    if content_type.startswith('text/html'):
        # 解析网页
        html = decode_html(resp.read(), content_type)

        # 1. 创建BeautifulSoupc对象
        bs = BeautifulSoup(html, 'lxml')

        # 2. 查询所有的a标签
        as_ = bs.find_all('a')
        for a_ in as_:  # a_ 是Tag对象
            # print(a_.text, a_.attrs.get('href'))
            href = a_.get('href')  # 同a_.attrs.get('href')
            if re.match(r'https://so.gushiwen.org/shiwenv_\w+?.aspx', href):
                print('-->', a_.getText(), href)  # 应该将url的请求和回调 存入到Queue队列中

    elif content_type.startswith('image/'):
        # 保存图片
        pass

    else:  # 非 网页或图片，最大的可能是json数据
        pass


def item_pipeline(**data):
    print(data)


def start_spider():
    download(url)


if __name__ == '__main__':
    start_spider()
