import re

import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:64.0) Gecko/20100101 Firefox/64.0',
    'Connection': 'keep-alive',
    'Cookie': 'BAIDUID=735509FECFADE32D9D0690BB937D157A:FG=1'
}

url = 'https://fanyi.baidu.com/transapi'


def transapi(keyword):

    if re.match(r'^[a-zA-Z]+$', keyword):
        from_, to_ = 'en', 'zh'
    elif re.match(r'^[\u4e00-\u9fa5]+$',keyword):
        from_, to_ = 'zh', 'en'
    else:
        print(f'输入的字符无法识： {keyword}')

    params = {
        'from':from_,
        'to': to_,
        'query': keyword,
        'source': 'txt'
    }

    resp = requests.request('post', url, data=params, headers=headers)
    if resp.status_code == 200:
        content_type = resp.headers.get('content-type')
        print(content_type)
        if content_type.startswith('application/json'):
            json = resp.json()
            print(json)


if __name__ == '__main__':
    transapi('春节')
