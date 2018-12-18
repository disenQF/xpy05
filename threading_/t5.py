from threading import Thread, local,current_thread


def t1():
    var.v = 100
    print(current_thread().name, '-本地变量->', var.v)
    var.v = 789
    print(current_thread().name, '-本地变量->', var.v)


if __name__ == '__main__':
    var = local()

    var.v = 123  # 主线程的本地变量
    t = Thread(target=t1)
    t.start()
    t.join()

    print(current_thread().name, '-本地变量->', var.v)