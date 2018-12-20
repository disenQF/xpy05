from threading import Thread
from urllib.request import HTTPHandler, build_opener, Request
from urllib.error import HTTPError
from urllib.parse import quote, urlencode

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

url = 'http://tieba.baidu.com/f'
headers = {
    'User-Agent': 'QF-XA-PY05-Spider'
}

params = {
    'kw': 'python3',
    'ie': 'utf-8',
    'pn': 150  # 0, 50, 100, 150
}

# 1. 声明HTTP处理器 - HTTPHandler
handler = HTTPHandler()

# 2. 构造opener 打开器（浏览器）
opener = build_opener(handler)


def search_tieba(keyword, page_num=0, filename=None):
    # 设置参数
    params['kw'] = keyword
    params['pn'] = page_num

    # 3. 实例化请求对象 Request
    req = Request(url,
                  data=urlencode(params).encode(),
                  headers=headers)

    # 4. 发送请求
    resp = opener.open(req)

    with open(filename, 'wb') as f:
        f.write(resp.read())

    print('--over--')


if __name__ == '__main__':
    keys = [('如何提高专注度', 't1.html'),
            ('记忆曲线图', 't2.html'),
            ('Python的岗位 ', 't3.html')]

    sts = [Thread(target=search_tieba,
                  kwargs={'keyword': k, 'filename': filename})
           for k, filename in keys]

    for t in sts:
        t.start()

    for t in sts:
        t.join()

    print('---所有任务完成---')
