import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement

options = Options()
options.add_argument('--headless')  # 无头-不显示浏览界面
options.add_argument('--disable-gpu')  # 禁用gpu

# options.binary_location = r'd:/chromedriver.exe'  # window下chrome驱动位置

# 创建chrome浏览器
# chrome_options 和 options两个参数同样的效果
# executable_path 参数设置 chromedriver.exe的路径， 【建议】将驱动的路径放在path环境变量中
browser = webdriver.Chrome()

# 通过浏览器打开网页
browser.get('https://www.baidu.com')
time.sleep(1)

# 查找相关的元素，执行点击事件
# 查找搜索框 <input id='kw' name='wd'>
input_element: WebElement = browser.find_element_by_id('kw')
input_element.send_keys('智联')  # 设置搜索框内容

# 查找 <input type='submit' id='su'>
button_su = browser.find_element_by_id('su')
button_su.click()  # 点击控件

time.sleep(5)

browser.save_screenshot('baidu_su.png')  # 截屏, 部分同学不支持截图

browser.close()  # 关闭网页
browser.quit()  # 退出浏览器
