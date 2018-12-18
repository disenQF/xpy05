from threading import Thread, current_thread
import os


def list_img(path):
    print(current_thread().name, '开始搜索 %s 中的图片' % path)
    if os.path.exists(path):
        for filename in os.listdir(path):
            # 判断filename是否为目录
            full_file_path = os.path.join(path, filename)
            if os.path.isdir(full_file_path): list_img(full_file_path)
            else:
                print(full_file_path)


if __name__ == '__main__':
    # 1. 创建线程
    t = Thread(target=list_img, args=('../images',))

    # 2. 运行线程
    t.start()

    # 3. 等待线程完成
    t.join()

    print('--over--')
