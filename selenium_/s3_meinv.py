"""
在Selenium执行js脚本
http://www.meinv.hk/
"""
import time
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement

chrome = webdriver.Chrome()

chrome.get('http://www.meinv.hk/')
time.sleep(2)

js_script = """
var d = document.documentElement.scrollTop = 10000;
"""
chrome.execute_script(js_script)

js_script ="""
var load_more = document.getElementById('fa-loadmore');
load_more.click()
"""

# 执行加载更多-脚本方式
chrome.execute_script(js_script)
time.sleep(2)
chrome.quit()

