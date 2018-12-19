import socket

if __name__ == '__main__':
    # 网络接口
    client = socket.socket()

    try:
        # 连接服务器
        # http 协议: 80端口
        # https 协议: 443 端口
        client.connect(('www.meinv.hk', 80))
        print('连接')

        # 发送 首页请求(get, / , http/1.1)
        # 发送数据（两部分）：
        #     第一是头部分，第二是body部分-post请求
        #     两个部分之间存在一个空行（代表头header结束 ）
        client.send('GET / HTTP/1.1\r\nHost:www.meinv.hk\r\nConnection:keep-alive\r\n\r\n'.encode())

        buffers = []
        while True:
            try:
                respone1 = client.recv(1024)  # 接收数据(字节数)
                buffers.append(respone1.decode())
                text:str = respone1.decode()
                if text.find('</html>') > 0:
                    break
                respone1 = None
            except:
                pass

        html = ''.join(buffers)
        print(html)

    except Exception as e:
        print(e)
        print('连接失败')