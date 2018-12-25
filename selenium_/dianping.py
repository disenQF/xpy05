"""
selenium -> switch_to_frame(frame)
从iframe标签中查找元素

https://account.dianping.com/login?redir=http%3A%2F%2Fwww.dianping.com%2F
"""
import time
from selenium import webdriver

driver = webdriver.Chrome()

driver.get('https://account.dianping.com/login?redir=http%3A%2F%2Fwww.dianping.com%2F')

# 获取iframe标签
iframe = driver.find_element_by_tag_name('iframe')
driver.switch_to.frame(iframe)  # 切换窗口(iframe内嵌窗口)
time.sleep(3)

span_login = driver.find_element_by_class_name('bottom-password-login')
print('--账号登录-->', span_login)
if span_login:
    span_login.click()

time.sleep(10)
driver.quit()
