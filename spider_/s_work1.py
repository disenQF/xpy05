import json
from urllib.error import URLError, HTTPError
from urllib.request import urlopen, Request
from urllib.parse import urlencode

url = 'http://www.kfc.com.cn/kfccda1/ashx/GetStoreList.ashx?op=cname'

headers = {
    'User-Agent': 'Postman-Mac Os'
}


def search_kfc(city_name, pageSize):
    params = {
        'cname': city_name,
        'pageSize': pageSize
    }

    try:
        resp = urlopen(Request(url,
                               urlencode(params).encode(),
                               headers))
    except HTTPError as e:
        # e.url 错误的url网址
        # e.code HTTP错误的代码 10x, 20x, 30x, 40x, 50x
        # e.msg 错误的详细说明
        print(e.url, e.code, e.msg)
        return

    json_txt = resp.read().decode()
    kfc_dict = json.loads(json_txt)
    print(kfc_dict)


search_kfc('安康', 20)