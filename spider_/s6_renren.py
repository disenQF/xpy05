from urllib.request import urlopen, urlretrieve, Request


# url = 'http://zhibo.renren.com/top'
url = 'http://www.renren.com/349584673'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:64.0) Gecko/20100101 Firefox/64.0',
    'Cookie': '_de=44B53BBC05E9DDCC045E9BEA11462C89677B8FA35C706602;_r01_=1;anonymid=jpvw3qih-i1heqz;ch_id=10016;depovince=GW;first_login_flag=1;ick_login=3ebfce24-c029-4208-b605-e93052e0716f;id=349584673;jebe_key=484bd825-be48-41cd-a79e-2b6d5657d811|97302957192bce1e484d2edf401535ce|1545274115646|1|1545274115752;jebecookies=bd530c76-957c-403a-a65e-cfcdb3a0ea59|||||;ln_hurl=http://hdn.xnimg.cn/photos/hdn421/20130407/2110/h_main_6vEK_4b3f0000034d111a.jpg;ln_uact=zhangyan100501@163.com;loginfrom=syshome;p=19a1d54a7d785cb0c77877c66fc9841b3;societyguester=03e73cd74ce67e292204ad218370d0d73;t=03e73cd74ce67e292204ad218370d0d73;wp=1;wp_fold=1;xnsid=367c433c'
}

req = Request(url, headers=headers)
# urlretrieve(req, 'renren.html') url不能是Request请求对象

resp = urlopen(req)
with open('renren-1.html', 'wb') as f:
    f.write(resp.read())

print('--ok-')
