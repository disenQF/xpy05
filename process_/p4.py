import uuid
from multiprocessing import Process, Pipe

import time
from requests import request

import os

'''
管道的用法
'''
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR = os.path.join(BASE_DIR, 'images')


def downloader(conn) -> None:
    while True:
        url = conn.recv()
        if url == '0':
            break
        print('正在下载: ', url)
        resp = request('get', url)
        print(resp.status_code)
        if resp.status_code == 200:
            # 请求成功
            # 获取响应的数据类型- MIME-Type
            # 常用数据类型: text/html,  text/css,text/plain, application/json
            #               image/jpeg,  image/png,  image/gif
            content_type = resp.headers.get('Content-Type')
            extName = '.jpg' if content_type.startswith('image/jpeg') \
                else '.png' if content_type.startswith('image/png') \
                else '.gif'

            filename = uuid.uuid4().hex + extName
            print('正在保存:', filename)
            with open(os.path.join(IMG_DIR, filename), 'wb') as f:
                f.write(resp.content)


if __name__ == '__main__':
    # 1. 创建管道Pipe
    conn1, conn2 = Pipe(duplex=False)  # False 表示半双工

    p = Process(target=downloader, args=(conn1,))
    p.start()

    # 读取urls.txt文件，拿到图片地址
    # python 的上下文：
    #  两个事件:
    #     1) 进入上下文： 调用对象的__enter__ 方法
    #     2) 退出上下文： 调用对象的__exit__  方法
    with open('urls.txt') as f:
        for line in f:  # 每次调用f的__next__ 方法
            conn2.send(line)
            time.sleep(5)

    conn2.send('0')  # 任务完成

    p.join()  # 等待子进程完成任务
    print('---over---')
