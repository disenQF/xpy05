"""
使用urllib.request实现简单的请求
1. 请求网页
2. 保存网页
3. 请求图片并保存图片
"""
import hashlib
from http.client import HTTPResponse
from urllib import request

import ssl
ssl._create_default_https_context = ssl._create_unverified_context


def baidu(path):
    # http:// 是HTTP协议的 schema
    # https:// 是HTTP+SSL协议的 schema
    # redis:// 是redis连接的 schema
    # ftp://  是FTP协议的schema
    url = 'http://www.baidu.com' + path

    resp: HTTPResponse = request.urlopen(url)

    # 判断请求是否成功
    if resp.code == 200:  # 响应状态代码
        print(resp.url, '--请求成功!--')
        print(type(resp))
        print(resp.status)  # 同resp.code
        print(resp.headers)

        # 请取响应的数据 read(), readline(), readlines()
        # print(resp.read())
        mine_type = resp.info().get('Content-Type')
        if mine_type.endswith('html'):
            ext_name = '.html'
        elif mine_type.endswith('jpeg'):
            ext_name = '.jpg'

        with open('baidu-'+path[1:]+ext_name, 'wb') as f:
            f.write(resp.read())

        print('网页保存成功!')
    else:
        print('--请求失败--', resp.code)


def csdn(path):
    url = 'https://www.csdn.net'+path

    filename = path[1:]
    if filename == '':
        filename = 'index.html'
    else:
        filename = filename + '.html'
    request.urlretrieve(url, 'csdn-'+filename)
    print('下载csdn', path, '网页成功!')


def save_img(url, filename):
    try:
        request.urlretrieve(url, filename)
        print(url, '--保存成功--', filename)
    except:
        print('保存失败')


def md5(url):
    m = hashlib.md5()
    m.update(url.encode())
    return m.hexdigest()


if __name__ == '__main__':
    # baidu('/')
    # csdn('/')
    url = 'https://attach.bbs.miui.com/forum/201602/07/071522tp5phhb11hfk8p5a.jpg.thumb.jpg'
    filename = md5(url)+'.'+url.split('.')[-1]

    save_img(url, filename)

