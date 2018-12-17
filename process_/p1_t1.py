from multiprocessing import Process



def test():
    # 如果此函数在子进程中执行，则会复到a到子进程的内存中
    global a  # 修改全局变量,
    a += 100
    print('子进程: a=', a, id(a))

a = 100

if __name__ == '__main__':
    p1 = Process(target=test)
    # p1.is_alive() -> False  # 是否存活， bool,
    p1.start()
    # p1.is_alive() -> True
    # print(p1.is_alive())
    # p1.terminate()  # 中断执行
    p1.join()

    print('父进程: a=', a, id(a))