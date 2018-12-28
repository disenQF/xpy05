import sys

def download(url):
    print('开始下载', url)

    # 程序在运行的过程中可能会出现的异常
    # 针对此异常，我们的程序并没有处理
    raise Exception('--下载超时-')


def global_except(except_type, msg, trackback):
    print('-------上报程序中断/异常信息------')
    print(except_type, msg)
    print(dir(trackback))
    # 显示当前异常帧frame
    print(trackback.tb_frame.f_lineno,
          trackback.tb_frame.f_code.co_name,
          trackback.tb_frame.f_locals)

    # 显示下一个常帧的跟踪位置信息
    print(trackback.tb_next.tb_frame.f_lineno,
          trackback.tb_frame.f_code.co_name,
          trackback.tb_next.tb_frame.f_locals)

    print(trackback.tb_next.tb_next)
    print('-----------------------')


if __name__ == '__main__':
    sys.excepthook = global_except
    download('http://www.baidu.com/s?kw=123')