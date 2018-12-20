from urllib.parse import urlencode
from urllib.request import HTTPCookieProcessor, Request, build_opener
from http.cookiejar import CookieJar

url = 'http://www.renren.com/ajaxLogin/login?1=1&uniqueTimestamp=20181141452439'

params = {
    'email': '',
    'icode': '',
    'origURL': 'http://www.renren.com/',
    'domail': 'www.renren.com',
    'key_id': 1,
    'captcha_type': 'web_login',
    'password': '',
    'rkey': '39b392090c635431e86ef76d46f31f40',
    'f': ''
}

headers = {
    'User-Agent': 'QF-XA-PY05-Spider'
}


def build_browser():  # [fn] + shift + F6 重构的重命名
    # 1. 创建Handler-> HTTPCookieProcessor(CookieJar)
    handler = HTTPCookieProcessor(CookieJar())  # 会保留Cookie的信息

    # 2. 创建opener
    return build_opener(handler)


def login(opener):
    req = Request(url, urlencode(params).encode(), headers)
    resp = opener.open(req)
    resp_txt = resp.read()
    print(resp_txt.decode())


def home(opener):
    #  登录成功后，再次请求时，会使用CookieJar中保存的cookie数据
    resp = opener.open('http://www.renren.com/top')
    with open('renren-index.html', 'wb') as f:
        f.write(resp.read())

    resp = opener.open('http://www.renren.com/349584673/profile')
    with open('renren-profile.html', 'wb') as f:
        f.write(resp.read())

    resp = opener.open('http://friend.renren.com/managefriends')
    with open('renren-friends.html', 'wb') as f:
        f.write(resp.read())


if __name__ == '__main__':
    browser = build_browser()
    login(browser)
    home(browser)
