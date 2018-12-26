import requests
from lxml import etree

cookies = 'QCCSESSID=r1sp0ug42ubc6ds63ljk4jutb5; UM_distinctid=167e596b2ba9-05be2d58a47f688-4a566b-fa000-167e596b2bb435; CNZZDATA1254842228=962441888-1545740896-%7C1545740896; zg_did=%7B%22did%22%3A%20%22167e596b56da6-00cb3361ad1c2d-4a566b-fa000-167e596b56e320%22%7D; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201545745118579%2C%22updated%22%3A%201545745318421%2C%22info%22%3A%201545745118587%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22cuid%22%3A%20%22093f6d45452e9aad1e822e1fcf969ef0%22%7D; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1545745119; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1545745319; hasShow=1; _uab_collina=154574511933519182266535; saveFpTip=true; acw_tc=2be0b8c915457451289767991e64d7d2b5b772f580269d43fb608734e0'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:64.0) Gecko/20100101 Firefox/64.0'
}


def convert_cookie():
    cookie_key_value = cookies.split(';')
    cookie_dict = {}
    for key_value in cookie_key_value:
        key, value = tuple(key_value.split('='))
        cookie_dict[key] = value

    return cookie_dict


def download(url):
    resp = requests.get(url, cookies=convert_cookie(), headers=headers)
    if resp.status_code == 200:
        return resp.text


def qcc(city):
    url = 'https://www.qichacha.com/g_%s' % city

    html = download(url)

    et = etree.HTML(html)
    as_ = et.xpath('//section[@id="searchlist"]/a')
    for a in as_:
        href = 'https://www.qichacha.com' + a.xpath('@href')[0]
        name = a.xpath('./span[2]/span/text()')[0]

        info_html = download(href)
        et_ = etree.HTML(info_html)
        cdes_list = et_.xpath('//span[@class="cvlu"]/span/text()')
        print(cdes_list)


if __name__ == '__main__':
    # print(convert_cookie())
    qcc('SAX')
