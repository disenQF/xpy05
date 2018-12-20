"""
爬取西刺代理ip
"""
import csv
from http.cookiejar import CookieJar
from urllib.request import urlopen, HTTPCookieProcessor, build_opener, Request, ProxyHandler
import re
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

url = 'https://www.xicidaili.com/nn/'  # https://www.xicidaili.com/nn/2

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:64.0) Gecko/20100101 Firefox/64.0'
}

opener = build_opener(HTTPCookieProcessor(CookieJar()),
                      ProxyHandler(proxies={'https': '180.118.242.86:61234'}))


def get():
    resp = opener.open(Request(url, headers=headers))

    html = resp.read()
    print(html.decode())
    with open('xc.html', 'wb') as f:
        f.write(html)

    print('--over--')


def parse():
    with open('xc.html') as f:
        html = f.read()  # 读取是text文本数据

    # 从html中读取所有 http类型， ip, port
    ip_list = re.findall(r'(\d+?\.\d+?\.\d+?\.\d+?)</td>\s+?.*?(\d{2,5})', html, re.M)
    http_list = re.findall(r'<td>(HTTP[S]?)</td>', html)
    # print(ip_list, len(ip_list), sep='\n')
    # print(http_list, len(http_list), sep='\n')

    proxy_ip_info = []
    for i in range(len(ip_list)):
        proxy_ip_info.append((http_list[i], *ip_list[i]))

    print(proxy_ip_info)

    with open('proxy_ip.csv', 'a') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=('schema', 'ip', 'port'))

        for schema, ip, port in proxy_ip_info:
            writer.writerow({'schema': schema,
                             'ip': ip,
                             'port': port})

        print('写入csvy文件成功！')


def read_proxy_id():
    with open('proxy_ip.csv', 'r') as f:
        reader = csv.DictReader(f, fieldnames=('schema', 'ip', 'port'))
        for row in reader:
            print(row.values())


if __name__ == '__main__':
    # get()
    # parse()
    read_proxy_id()
