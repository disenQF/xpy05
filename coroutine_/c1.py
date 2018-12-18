'''
基于yield/send
'''
import random
import time


def fib(top_n):
    a, b = 0, 1
    index = 1
    while index <= top_n:
        # delay 从外部传入的延迟时间
        delay = yield b  # 返回第index位置的数
        print('---休息--', delay)
        time.sleep(delay)
        a, b = b, a+b
        index += 1


if __name__ == '__main__':
    # for n in fib(10):
    #     print(n)
    f = fib(10)  # 生成器对象
    n = next(f)  # 从fib内获取数据
    print(n)
    print('--我 隔了两天--')
    time.sleep(1)
    while True:
        try:
            n = f.send(random.uniform(0.5, 1.5))  # 先向fib发送数据， 再从fib内获取数据
            print('获取的数据:', n)
        except:
            break