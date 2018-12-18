from threading import Thread, Lock, Condition, current_thread
from queue import Queue

import time


class ConcurrentQueue():
    def __init__(self, max_size=10):
        self.max_size = max_size

        # Condition-> acquire(), release(), wait(), notify()
        self.condition = Condition(Lock())  # 条件变量
        self.q = Queue()

    def get(self):  # 销售
        with self.condition:
            while self.q.empty():
                print('销售', current_thread().name, '仓库为空的...')
                self.condition.wait(timeout=30)

            # 当前不为空, 仓库有存货
            obj = self.q.get()
            self.condition.notify()  # 通知 生产线程可以再生产了
        return obj

    def put(self, obj):  # 生产
        with self.condition:
            while self.q.qsize() >= self.max_size:
                print('生产', current_thread().name, '仓库已满...')
                self.condition.wait()  # 等待销售的notify

            self.q.put(obj)
            self.condition.notify()  # 通知销售线程，可以继续销售


def producer(q, start, end):
    for _ in range(start, end):
        obj = '黄金-%d' % _
        print('生产者：', current_thread().name, obj)
        q.put(obj)  # 如果仓库满时，则会阻塞
        time.sleep(0.1)


def consumer(q):
    for _ in range(500):
        obj = q.get()
        print('消费者：', current_thread().name, obj)
        time.sleep(0.2)


def start_thread(threads):  # 启动所有线程
    for t in threads:
        t.start()


def wait_all(threads):  # 等待所有线程结束
    for t in threads:
        t.join()


if __name__ == '__main__':
    q = ConcurrentQueue(100)

    seq = ((1000, 2000),
           (3000, 4000),
           (5000, 6000))
    # 创建三个生产线程
    ps = [Thread(target=producer, args=(q, *seq[_])) for _ in range(3)]

    # 创建五个销售线程
    cs = [Thread(target=consumer, args=(q,)) for _ in range(5)]

    start_thread(ps+cs)
    wait_all(ps+cs)

    print('--over---')