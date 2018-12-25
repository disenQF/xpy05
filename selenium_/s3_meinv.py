"""
在Selenium执行js脚本
http://www.meinv.hk/
"""
import time
from selenium import webdriver

chrome = webdriver.Chrome()

chrome.get('http://www.meinv.hk/')
time.sleep(2)

js_script = """
var d = document.documentElement.scrollTop = 10000;
"""
chrome.execute_script(js_script)

load_more = chrome.find_element_by_xpath('//button[@id="fa-loadmore"]')
print(load_more)
load_more.click()
time.sleep(2)
chrome.execute_script(js_script)
time.sleep(2)
chrome.quit()

