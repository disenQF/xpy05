"""
selenium -> switch_to_frame(frame)
从iframe标签中查找元素

https://account.dianping.com/login?redir=http%3A%2F%2Fwww.dianping.com%2F
"""
import time
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.common.touch_actions import Command


driver = webdriver.Chrome()  # 2.38.552518 -> chrome=71.0.3578.98

driver.get('https://account.dianping.com/login?redir=http%3A%2F%2Fwww.dianping.com%2F')

# driver.execute(Command.MOVE_TO, {'', })

# 获取iframe标签
iframe = driver.find_element_by_tag_name('iframe')
# driver.switch_to.frame(iframe)  # 切换窗口(iframe内嵌窗口)
driver.switch_to.frame(iframe)
time.sleep(3)

span_login = driver.find_element_by_class_name('icon-qrcode')
print('--账号登录-->', span_login)
if span_login:
    span_login.click()

time.sleep(10)
driver.quit()
