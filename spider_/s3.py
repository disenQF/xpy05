"""
使用 urllib.parse模块
解决： url请求参数中的中文编码问题

1. quota : 将中文进行url编码
2. unquota: 将url编码进行解码
2. urlencode: 将完整的url中参数进行编码
"""

from urllib.parse import quote, urlencode, unquote
from urllib.request import urlopen, urlretrieve
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


def test():
    params = {
        'word': '荷花',
        'od': '花',
        'tn': 'baiduimage'
    }
    print(urlencode(params))


def baidu_search(keyword):
    # encoded_params = 'word=%E8%82%89%E5%A4%B9%E9%A6%8D'
    # params = unquote(encoded_params)
    # print(params)
    keyword_encode = quote(keyword)
    url = 'https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1545203556140_R&pv=&ic=&nc=1&z=&hd=&latest=&copyright=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word={}&f=3&rsp=0'.format(keyword_encode)

    # resp = urlopen(url)
    # print(resp.read().decode())
    urlretrieve(url, 'flower.html')


if __name__ == '__main__':
    # baidu_search('荷花')
    test()