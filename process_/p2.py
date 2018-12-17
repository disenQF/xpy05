'''
生成1000个随机4位验证码（由字母和数字组成）
每间隔2秒中读取一次验证码（统计验证码的数量）
'''
import re
from multiprocessing import Process, current_process
import os
import string
import random

import time


def random_verify_code(total_cnt=1000, length=4, file_path=None):
    if file_path is not None:
        random_range = string.ascii_uppercase + string.digits
        l = list(random_range)

        for _ in range(total_cnt):
            random.shuffle(l)  # 打乱顺序

            # 找出前len位不重复的字符
            verify_code = set()
            index = 0
            while len(verify_code) < length:
                verify_code.add(l[index])
                index += 1

            verify_code = ''.join(verify_code)
            with open(file_path, 'a') as f:
                f.write(verify_code+'\n')

            time.sleep(0.1)

    # current_process() 获取当前进程的对象
    print(current_process().name, current_process().pid, '-生成任务完成--')


def count_verfiy_code(delta=2, file_path=None):
    time.sleep(1)
    if file_path is not None:
        last_lines = 0
        while True:
            # 统计指定文件的代码行数  wc
            r = os.popen('cat %s |wc -l' % file_path)
            lines = r.read()
            lines = int(re.findall(r'\d+', lines)[0])
            print(lines, last_lines)
            if lines == last_lines:  # 比较的类型保持一致
                break
            print(lines)  # 读取命令的结果
            last_lines = lines
            time.sleep(delta)

            # 什么时候停止:
            #      比较上一次读取的行数是否相同，如果相同则break


if __name__ == '__main__':
    p1_param = {
        'total_cnt': 100,
        'file_path': 'verify_code.txt'
    }

    p2_param = {
        'file_path': 'verify_code.txt'
    }

    p1 = Process(target=random_verify_code, kwargs=p1_param)
    p2 = Process(target=count_verfiy_code, kwargs=p2_param)

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print('---over---')