import uuid
from multiprocessing import Process, Queue

import time
from requests import request
import os
import re

from process_.p4 import IMG_DIR


def spider_img(url, queue: Queue):  # 爬虫网页下载图片
    print('-->开始爬取：', url)
    resp = request('get', url)
    html = resp.text
    # 人名   <h1 class="title">舒畅</h1>
    name = re.findall(r'<h1 class="title">(.*?)</h1>', html)[0]
    # 获取所有图片的地址
    images_div = re.findall(r'<div class="post-image">(.*?)</div>', html)[0]
    images = re.findall(r'src="(.*?)"', images_div)

    for img_url in images:
        resp = request('get', img_url)
        queue.put((name, img_url, resp.content))
        print('下载%s 完成' % img_url)
        time.sleep(1)

    print('')


def pipeline(queue: Queue):  # 保存图片
    while True:
        try:
            name, url, bytes = queue.get(timeout=30)  # 如果在30秒内拿不到数据，则会抛出异常
            dir_ = os.path.join(IMG_DIR, name)
            if not os.path.exists(dir_):
                # os.makedirs()
                os.mkdir(dir_)

            with open(os.path.join(dir_, uuid.uuid4().hex+'.jpg'), 'wb') as f:
                f.write(bytes)

            print('-保存图片--', url)
        except:
            break


if __name__ == '__main__':
    q = Queue(maxsize=10)  # varchar(20) 20表示字符的长度，不是字节

    start_url = 'http://www.meinv.hk/?p=2719'
    spider = Process(target=spider_img,
                     args=(start_url, q))

    pipeline_ = Process(target=pipeline, args=(q,))

    spider.start()
    pipeline_.start()

    spider.join()
    pipeline_.join()

    print('---over--')  # 生成爬虫报告
