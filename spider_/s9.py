"""
代理的设置
ProxyHandler

? build_opener()是否支持多个Handler
"""

from urllib.request import ProxyHandler, Request, build_opener, HTTPCookieProcessor
from http.cookiejar import CookieJar

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def build_browser():
    cookie_handler = HTTPCookieProcessor(CookieJar())
    proxy_handler = ProxyHandler(proxies={
        'https': '27.208.83.27:8118'
    })

    opener = build_opener(proxy_handler, cookie_handler)
    return opener


def get(url, opener):
    req = Request(url)
    resp = opener.open(req)
    with open('ip-xc.html', 'wb') as f:
        f.write(resp.read())

    print('---保存成功---')


if __name__ == '__main__':
    opener = build_browser()
    get('http://www.baidu.com', opener)