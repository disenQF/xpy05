"""
买家秀-模特信息爬取
"""
import re
from urllib.request import urlopen, Request
import csv
import os

from threading import Thread
from queue import Queue

import time
from lxml import etree

user_agent = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:64.0) Gecko/20100101 Firefox/64.0',
              'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko)'
              ' Chrome/71.0.3578.98 Safari/537.36']


def start_spider(task_q, img_q):
    while True:
        try:
            url = task_q.get(timeout=60)
            resp = urlopen(Request(url, headers={'User-Agent': user_agent[1]}))
            if resp.code == 200:
                print('请求', url, 'ok')
                parse(resp, img_q)
        except:
            break


def parse(resp, img_q):
    try:
        charset = resp.headers.get('Content-Type').split(";")[-1]  # text/html;charset=gbk
        bytes = resp.read()  # 读取响应的字节数据
        if charset:
            encoding = charset.split('=')[-1]
            html = bytes.decode(encoding=encoding)
        else:
            html = bytes.decode()
    except Exception as e:
        print(e)
        return

    # 解析数据
    et = etree.HTML(html)  # Element对象
    li_es = et.xpath('//li[starts-with(@class, "deanactions")]')  # li标签的Element的列表
    try:
        mt_info = {}
        for li in li_es:
            mt_info['info_href'] = 'http://www.tbqq.net/' + li.xpath('./a/@href')[0]
            mt_info['img_src'] = 'http://www.tbqq.net/' + li.xpath('.//img/@src')[0]
            mt_info['name'] = li.xpath('.//div[@class="deanmadouname"]/a/text()')[0]
            mt_info['zhiye'] = li.xpath('.//div[@class="deanmadouzhiye"]/span/text()')[0]
            mt_info['height'], mt_info['weight'] = tuple(li.xpath('.//div[@class="deanmdl"]/span/text()'))
            mt_info['hearts'] = li.xpath('.//div[@class="deanmdr"]/span/text()')[0]
            mt_info['city'] = li.xpath('.//div[@class="deanmadouinfos"]/div[last()]/text()')[0]

            item_pipeline(img_q, **mt_info)  # 保存数据

    except Exception as e:
        print(e)


def save_img(img_q):
    while True:
        try:
            url, name = img_q.get(timeout=60)
        except:
            break

        resp = urlopen(Request(url, headers={'User-Agent': user_agent[1]}))
        content_type = resp.headers.get('Content-Type')
        if content_type.startswith('image/jpeg'):
            name += '.jpg'
        elif content_type.startswith('image/png'):
            name += '.png'
        else:
            name += '.gif'

        with open('images/%s' % name, 'wb') as f:
            f.write(resp.read())

        print(url, '保存图片成功:')


def item_pipeline(img_q, **data):
    city = data['city']
    data['city'] = city[city.index(':')+1: city.rindex('\r\n')]

    with open('mjx_mt.csv', 'a') as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        writer.writerow(data)

    # 下载图片
    img_q.put((data['img_src'], data['name']))


def spider_link(q, start_url):  # 爬取所有网页连接
    q.put(start_url)

    for page in range(2, 100):
        url = 'http://www.tbqq.net/forum.php?mod=forumdisplay&fid=2&sortid=2&sortid=2&page=%d' % page
        time.sleep(10)
        q.put(url)


if __name__ == '__main__':
    task_queue = Queue()  # 爬虫网页队列
    img_queue = Queue()  # 下载图片队列

    # start_spider('http://www.tbqq.net/')

    link_thread = Thread(target=spider_link, args=(task_queue, 'http://www.tbqq.net/'))
    link_thread.start()

    spider_thread = Thread(target=start_spider,
                           args=(task_queue, img_queue))
    spider_thread.start()

    img_thread = Thread(target=save_img, args=(img_queue, ))
    img_thread.start()

    link_thread.join()
    spider_thread.join()
    img_thread.join()

    print('---over---')
