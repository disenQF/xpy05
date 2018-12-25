"""
晒了吗， 爬取所有模特信息
https://www.shailema.com/views/home/hall-show.html
"""
import re
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.remote.webelement import WebElement

chrome = webdriver.Chrome()  # chromedriver驱动已放在path或/usr/local/bin目录下


def start_spider():
    start_url = 'https://www.shailema.com/views/home/hall-show.html'
    download_middle(start_url, parse_mt)


def download_middle(url, callback):
    chrome.get(url)  # 会阻塞到网页请求完成

    # 获取网页的内容
    html = chrome.page_source

    callback(html)  # 可以考虑异步方式

    time.sleep(10)

    # 换一批
    for _ in range(10):
        renovate: WebElement= chrome.find_element_by_class_name('renovate')
        renovate.click()
        callback(chrome.page_source)
        time.sleep(5)


def parse_mt(html):
    soup = BeautifulSoup(html, 'lxml')
    model_items = soup.select('.modelItem')  # list[Tag, ...,Tag]
    for model_item in model_items:
        a = model_item.find('a')
        detail_href = 'https://www.shailema.com/views/home/' + a.get('href')
        img_src = 'https://www.shailema.com'+ a.find('img').get('src')[5:]

        info_ps = model_item.find('div', class_='informationBox').select('p')  # list[Tag,....,Tag]
        info = []
        for info_p in info_ps:
            info.append(info_p.text.split('：')[-1])

        height, weight, age, city = tuple(info)

        name_p = model_item.find('p', class_='name')
        name = name_p.text

        sex_src = name_p.find('img').get('src')  # str
        sex = '女' if sex_src.find('boy') == -1 else '男'

        item_pipeline(**{
            'name': name,
            'sex': sex,
            'age': re.search(r'\d+', age).group(),
            'height': height,
            'weight': weight,
            'city': city,
            'detail_href': detail_href,
            'img_src': img_src
        })


def item_pipeline(**data):
    print(data)


if __name__ == '__main__':
    start_spider()