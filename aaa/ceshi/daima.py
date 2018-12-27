from PIL import Image
from scrapy.http import HtmlResponse
from selenium.webdriver.chrome.options import Options
import time
from ceshi.python3 import YDMHttp

#导入驱动接口
from selenium import webdriver
class SeleniumMiddleware(object):
    def __init__(self):
        self.chrome_options = Options()
        # self.chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()  # 将浏览器最大化
    def process_request(self,request,spider):
        used_selenium = request.meta.get('used_selenium', False)

        if used_selenium:
            if request.meta.get('pageType', '') == 'login':
                # 证书编号
                bianma_ = "127751201806002652"
                # 姓名
                name_ = "樊志林"
                # 原始的url
                url= request.url

                self.driver.get(url)

                # 验证码处理
                username = 'maomaolin'

                # 密码
                password = 'fan427329'

                # 软件ＩＤ，开发者分成必要参数。登录开发者后台【我的软件】获得！
                appid = 6463

                # 软件密钥，开发者分成必要参数。登录开发者后台【我的软件】获得！
                appkey = '476bdeb9c71448f8a630ff2d99ba57f0'

                # 图片文件
                filename = 'save.png'

                # 验证码类型，# 例：1004表示4位字母数字，不同类型收费不同。请准确填写，否则影响识别率。在此查询所有类型 http://www.yundama.com/price.html
                codetype = 5000

                # 超时时间，秒
                timeout = 60

                while True:
                    try:
                        url1 = self.driver.current_url
                        print(url1)
                    except NotADirectoryError:
                        break
                    if  url1 == 'https://www.chsi.com.cn/xlcx/lscx/query.do':
                        # # 刷新页面
                        # self.driver.refresh()
                        # 点击获取验证码
                        self.driver.find_element_by_xpath('//input[@id="yzm"]').click()
                        imgelement = self.driver.find_element_by_xpath('//img[@id="captchImage"]')  # 定位验证码
                        self.driver.save_screenshot('screen1.png')
                        location = imgelement.location  # 获取验证码x,y轴坐标
                        print(location)
                        size = imgelement.size  # 获取验证码的长宽
                        print(size)
                        rangle = (int(location['x']), int(location['y']), int(location['x'] + size['width']),
                                  int(location['y'] + size['height']))  # 写成我们需要截取的位置坐标
                        i = Image.open("screen1.png")  # 打开截图

                        frame4 = i.crop(rangle)  # 使用Image的crop函数，从截图中再次截取我们需要的区域
                        frame4.save('save.png')  # 保存我们接下来的验证码图片 进行打码
                        # 检查
                        if (username == 'username'):
                            print('请设置好相关参数再测试')
                        else:
                            # 初始化
                            yundama = YDMHttp(username, password, appid, appkey)

                            # 登陆云打码
                            uid = yundama.login()
                            print('uid: %s' % uid)

                            # 查询余额
                            balance = yundama.balance()
                            print('balance: %s' % balance)

                            # 开始识别，图片路径，验证码类型ID，超时时间（秒），识别结果
                            cid, result = yundama.decode(filename, codetype, timeout)
                            yzm = []
                            for n in result:
                                if "a" <= n <= "z":
                                    yzm.append(n)
                                elif "A" <= n <= "Z":
                                    yzm.append(n.lower())
                                else:
                                    yzm.append(n)
                            yzm1 = "".join(yzm)
                            print(yzm1)
                            # 输入毕业证编码
                            bianma = self.driver.find_element_by_xpath("//input[@id='zsbh']")
                            bianma.clear()
                            bianma.send_keys(bianma_)
                            # 输入姓名
                            name = self.driver.find_element_by_xpath("//input[@id='xm']")
                            name.clear()
                            name.send_keys(name_)
                            # 输入验证码
                            state = self.driver.find_element_by_xpath('//input[@id="yzm"]')
                            state.send_keys(yzm1)
                            time.sleep(2)

                            # 点击免费查询
                            self.driver.find_element_by_xpath("//input[@id='xueliSubmit']").click()
                            time.sleep(3)
                    else:
                        phone = '18091044294'
                        self.driver.find_element_by_xpath("//input[@id='mphone']").send_keys(phone)
                        time.sleep(1)
                        # 点击获取手机验证码
                        self.driver.find_element_by_xpath("//input[@id='mphone_messagesend_btn']").click()
                        time.sleep(2)
                        self.driver.save_screenshot('screen2.png')
                        # 关闭
                        self.driver.find_element_by_xpath("/html/body/div[5]/div/table/tbody/tr[3]/td/div[2]/button").click()

                        url = self.driver.current_url
                        print(url)
                        return HtmlResponse(url, body=self.driver.page_source.encode(), status=200)
