"""
发起post请求,定制headers请求头
1.  urllib.request.Request(url, data, headers)
    data 如果不为空，表示Request的方法是post,反之为get

2. 针对data数据进行 urlencode编码

需求： 百度翻译 'https://fanyi.baidu.com/transapi'

"""
import json
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote
import ssl

import time

ssl._create_default_https_context = ssl._create_unverified_context

# 定义请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:64.0) Gecko/20100101 Firefox/64.0',
    'Connection': 'keep-alive',
    'Cookie': 'BAIDUID=735509FECFADE32D9D0690BB937D157A:FG=1'
}

url = 'https://fanyi.baidu.com/transapi'


def query(word, from_lang, to_lang):
    # 表单数据
    data = {
        'from': from_lang,
        'to': to_lang,
        'query': word,
        'source': 'txt'
    }

    # 生成post请求， data 是字典还是 from=en&to=zh格式？
    # data 是 from=en&to=zh格式的字节码
    request = Request(url,
                      urlencode(data).encode(),
                      headers)

    # 发起请求
    try:
        resp = urlopen(request)

        # json.loads() 是将json格式的字符串转成dict或list -> 反序列化
        json_ = json.loads(resp.read().decode())
        print(json_)
        return json_

    except Exception as e:
        print(e)


if __name__ == '__main__':
    query('python', 'en', 'zh')