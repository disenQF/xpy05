from threading import Thread, Lock, current_thread


def add():
    global money
    with lock:  # 加锁
        money += 100
        print(current_thread().name, 'money:', money)
        print(100/0)  # 会报异常

        # lock.release()  # 释放锁


def sub():
    global money
    for _ in range(3):
        print(current_thread().name,'----for-----')
        if lock.acquire():
            money -= 1
            print(current_thread().name, 'money:', money)
            lock.release()


if __name__ == '__main__':
    lock = Lock()

    money = 100

    t1 = Thread(target=add)
    t2 = Thread(target=sub)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print('---over--')
