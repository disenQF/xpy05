from multiprocessing import Process
import os

import time


def find_py(path):
    # 查看当前进程的id -> pid?
    # 父进程的id -> ppid
    print('当前进程id: ', os.getpid(),
          '当前父进程id: ', os.getppid())

    print('-开始查找-', path)   #  真正开发或生产环境下，必须使用logging日志

    time.sleep(3)
    # 判断path的目录是否存在
    if not os.path.exists(path):
        raise FileNotFoundError('文件未找到:', path)

    files = list(filter(lambda filename: filename.endswith('.py'),
                        os.listdir(path)))

    print(files)


if __name__ == '__main__':  # 程序的入口，类似于c/java 的 main 函数
    # pass  # 保持格式，空内容
    # find_py('/Users/apple/Desktop1')
    # find_py('/Users/apple/Desktop2')
    # find_py('/Users/apple/Desktop3')
    # find_py('/Users/apple/Desktop4')
    # 使用多进程来实现并行运行程序
    # 查看当前进程的id -> pid ?
    # 查看当前进的父进程的id -> ppid ?
    print('当前进程id: ', os.getpid(),
          '当前父进程id: ', os.getppid())

    # 1. 创建进程
    p1 = Process(target=find_py,
                 kwargs={'path': '/Users/apple/Desktop'})

    # 2. 启动进程-》就绪
    p1.start()

    # 3. 当前进程（父进程）要等待子进程结束
    p1.join(timeout=5)  # 可以指定等待的超时时长，单位：秒

    print('--所有任务执行完成--')

