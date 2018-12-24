"""
https://www.gushiwen.org/gushi/sanbai.aspx
基于beautifulSoupr爬取古诗文
"""
import random
import re
from queue import Queue
from threading import Thread, current_thread
from urllib.error import HTTPError
from urllib.request import Request, urlopen, ProxyHandler, build_opener

import time
from bs4 import BeautifulSoup, Tag

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from bs4_.utils import decode_html

url = 'https://www.gushiwen.org/gushi/sanbai.aspx'
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:32.0) Gecko/20100101 Firefox/32.0'

headers = {
    'User-Agent': user_agent
}

opener = build_opener(ProxyHandler(proxies={'http': '119.101.115.166:9999'}))

def download(queue):
    while True:
        try:
            # 从任务队列中读取任务(url, parse函数)
            url, callback = queue.get(timeout=30)
            resp = opener.open(Request(url, headers=headers))
            if resp.code == 200:
                print(f'request {url} ok')  # format格式字符串-> python 3.6+
                callback(resp, queue)
            else:
                print(f'request {url} fail: {resp.code}')  # 20x

            time.sleep(random.uniform(5, 10))
        except HTTPError as e:
            print(e)
        except Exception as e:
            break
    print(current_thread().name, '--over--')


def parse(resp, q):
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
                q.put((href, parse_book))  # 向任务队列中添加新的下载任务
    elif content_type.startswith('image/'):
        # 保存图片
        pass

    else:  # 非 网页或图片，最大的可能是json数据
        pass


def parse_book(resp, q):  # 第二层网页解析
    print(resp.url, '开始解析')
    html = decode_html(resp.read(), resp.headers.get('Content-Type'))

    bs = BeautifulSoup(html, 'lxml')
    h1: Tag = bs.find('h1')
    if h1:
       title = h1.text

    p: Tag = bs.find('p', class_='source')  # 返回第一个class为source的p标签
    if p:
        source = p.text

    div: Tag = bs.find('div', class_='contson') # 返回第一个class为contson的div标签
    if div:
        content = div.text

    item_pipeline(**{
        'title': title,
        'source': source,
        'content': content
    })


def item_pipeline(**data):  # 作业：将数据存放到mongodb中(库、集合、文档)
    print(data)


def start_spider(q):
    q.put((url, parse))  # 第一个任务-爬虫的入口

    download_threads = [Thread(target=download, args=(q, )) for _ in range(2)]
    for t in download_threads:  # 启动下载线程
        t.start()

    for t in download_threads:  # 等待下载线程结束
        t.join()

    print('---所有下载完成--')


if __name__ == '__main__':
    queue = Queue()
    start_spider(queue)
