'''
多线程共享进程的内存
通过Lock锁 解决一致性 问题：
    每一个线程操作的共享变量 "可能" 不一致
'''
from threading import Thread, current_thread, Lock

import time


def add(money):  # 存钱
    c_t = current_thread()
    print(c_t.name, '----进入存钱业务---')
    global my_money

    with lock:
        print(c_t.name, '余额', my_money, '本次存入:', money)
        my_money += money
        time.sleep(0.5)
        print(c_t.name, '余额', my_money)


def sub(money):  # 取钱
    c_t = current_thread()
    print(c_t.name, '----进入取钱业务---')
    global my_money

    # 进入上下文： 调用lock.acquire()  加锁
    # 退出上下文： 调用lock.release()  释放锁
    with lock:
        print(c_t.name, '余额', my_money, '本次取出:', money)

        # 如果其它线程修改 my_money ,则要等待 lock释放锁
        my_money -= money

        time.sleep(0.5)
        print(c_t.name, '余额', my_money)


if __name__ == '__main__':
    # 当前是主线程:  MainThread
    mt = current_thread()  # 获取当前线程
    print(mt.name, '运行ok')

    my_money = 100
    lock = Lock()

    add_t = Thread(target=add, args=(1000, ))
    sub_t = Thread(target=sub, args=(1000,))

    add_t.start()
    sub_t.start()

    add_t.join()
    sub_t.join()

    print(mt.name, '余额:', my_money)