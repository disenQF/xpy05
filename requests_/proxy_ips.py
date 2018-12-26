import requests

def get_proxy_ip():
    url = 'http://39.108.59.38:7772/Tools/proxyIP.ashx?OrderNumber=c23f2b154df29ff21c36382c6077f1a0&poolIndex=67923&cache=1&&Split=JSON2&qty=1'
    resp = requests.get(url)

    json_data = resp.json()
    proxy = json_data.get('Data')[0]
    ip, port = proxy.get('Ip'), proxy.get('Port')

    return '%s:%s' %(ip,port)


def test_proxy(proxy_ip_port):
    try:
        resp = requests.get('http://www.baidu.com', proxies={'http': proxy_ip_port})
        if resp.status_code == 200:
            print(proxy_ip_port, '--验证成功--')
    except:
        print(proxy_ip_port, '--验证失败--')


if __name__ == '__main__':
    for i in range(100):
        proxy_ip = get_proxy_ip()
        test_proxy(proxy_ip)