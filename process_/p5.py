import random
from multiprocessing import Process, Pipe

import time


def client(conn):
    while True:
        msg = conn.recv()  # 接收消息
        if msg == 'bye':
            break
        print('客户端: ', msg)

        conn.send(random.uniform(1, 3))  # 随机生成[1, 3)小数

    print('client over')


def server(conn):
    for _ in range(10):
        conn.send('hi, %d' % _ )
        delta_time = conn.recv()  # ? 读取是字符串还是数值类型
        time.sleep(delta_time)

    conn.send('bye')  # 发送结束信号


if __name__ == '__main__':
    conn1, conn2 = Pipe()  # 全双工

    p_client = Process(target=client, args=(conn1,))
    p_client.start()

    p_server = Process(target=server, args=(conn2, ))
    p_server.start()

    p_server.join()
    p_client.join()

    print('--over---')