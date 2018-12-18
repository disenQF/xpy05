'''
多线程共享进程的内存
问题：
    每一个线程操作的共享变量 "可能" 不一致
注意： 每次分配的CPU执行时间，基本满足执行100行左右的代码
'''
from threading import Thread, current_thread

import time


def add(money):  # 存钱
    global my_money
    c_t = current_thread()
    print(c_t.name, '余额', my_money, '本次存入:', money)
    my_money += money
    # time.sleep(0.5)
    print(c_t.name, '余额', my_money)


def sub(money):  # 取钱
    global my_money
    c_t = current_thread()
    print(c_t.name, '余额', my_money, '本次取出:', money)
    my_money -= money
    # time.sleep(0.5)
    print(c_t.name, '余额', my_money)


if __name__ == '__main__':
    # 当前是主线程:  MainThread
    mt = current_thread()  # 获取当前线程
    print(mt.name, '运行ok')

    my_money = 100

    add_t = Thread(target=add, args=(1000, ))
    sub_t = Thread(target=sub, args=(1000,))

    add_t.start()
    sub_t.start()

    add_t.join()
    sub_t.join()

    print(mt.name, '余额:', my_money)