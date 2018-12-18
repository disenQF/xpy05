import random
import string
from threading import Thread, current_thread, Lock

'''
线程类的写法： 继承Thread, 重写run()函数
'''

# 扩展： 多继承情况下，
#        调用super()据MRO编排的顺序依次调用父类的指定方法


class StackThread(Thread):
    def __init__(self):
        super().__init__()  # 调用父类的线程初始化函数

    def run(self):
        opt = random.randint(0, 1)
        print(self.name, stack, '压入' if opt else '弹出')
        # 判断是否取消操作
        if len(stack) == 0 and opt == 0:
            print(self.name, '本次操作取消')
            return
        with lock:  # 加锁
            if opt:
                stack.insert(0, random.choice(string.ascii_uppercase))
            else:
                print(self.name, stack.pop(0))

            print(self.name, stack)


if __name__ == '__main__':
    mt = current_thread()  # 获取当前主线程对象
    print(mt)

    stack = []  # 栈结构， 随机间隔时间，对stack压入或弹出操作

    lock = Lock()

    # 创建100线程
    threads = [StackThread() for _ in range(100)]

    # 启动线程
    for thread in threads:
        thread.start()

    # 等待线程完成
    for thread in threads:
        thread.join()

    print(mt.name, '--over--')