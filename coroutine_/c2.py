import asyncio
import re
import uuid

import requests


@asyncio.coroutine
def spider(start_url):
    print('启动爬虫')
    resp = yield from download(start_url)
    html = resp.text
    images_div = re.findall(r'<div class="post-image">(.*?)</div>', html)[0]
    images = re.findall(r'src="(.*?)"', images_div)
    for img_url in images:
        img_resp = yield from download(img_url)
        yield from save(img_url,
                        img_resp.content,
                        img_resp.headers.get('Content-Type'))

@asyncio.coroutine
def download(url):
    print('download', url)
    resp = requests.get(url)
    if resp.status_code == 200:
        print('download ok')
        return resp
    else:
        print('请求失败', url)


@asyncio.coroutine
def save(url, bytes, content_type):
    print('save-image', url)
    filename = uuid.uuid4().hex+'.jpg'
    with open(filename, 'wb') as f:
        f.write(bytes)


if __name__ == '__main__':
    # 创建一个事件模型对象 loop
    loop = asyncio.get_event_loop()

    # 启动协程，直到协程运行完成
    s1 = spider('http://www.meinv.hk/?p=2719')
    s2 = spider('http://www.meinv.hk/?p=2749')
    s3 = spider('http://www.meinv.hk/?p=2707')

    loop.run_until_complete(asyncio.wait([s1, s2, s3]))

    # 关闭模型
    loop.close()