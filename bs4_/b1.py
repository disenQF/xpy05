"""
https://www.gushiwen.org/gushi/sanbai.aspx
基于beautifulSoupr爬取古诗文
"""
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

        # 2. 查询每一个诗词分类
        # div: Tag = bs.find('div', class_='bookMl')
        book_mls = bs.find_all('div', class_='bookMl')  # bs4.element.Tag
        for div in book_mls:
            print(div.text, div.string, div.contents)

            # 获取所有的兄弟标签( span )
            for sib in div.next_siblings:  # generator [NavigableString, Tag, None]
                if isinstance(sib, Tag):
                    # print(sib.text, sib.find('a').get('href'))
                    item_pipeline(**{
                        'type_name': div.text,
                        'book_name': sib.text,
                        'book_url': sib.find('a').get('href')
                    })


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
