import logging
from logging.handlers import HTTPHandler
from unittest import TestCase

"""
1、日志的组成部分
   1) 记录器 logger 
   2) 处理器 handler
   3) 格式化 formatter
   4) 过滤器 filter
   
2、日志的等级 level
   1) FATAL = CRITICAL = 50  严重错误，导致系统崩溃的错误
   2) ERROR = 40             错误
   3) WARN = WARNING = 30    警告
   4) INFO = 20              普通信息
   5) DEBUG = 10             调试信息
   6) NOTSET = 0             没有设置，默认
   
   如果设置的等级是ERROR, 对于低于这个等级的信息则不会显示出来
"""

# 获取日志记录器，并且设置记录器的等级为 INFO
# getLogger(name) # name表示日志记录器的名称
# ？ django/flask框架中日志记录器的名称是什么?
# name如果为空，即没有指定，默认为 root
logging.getLogger().setLevel(logging.INFO)

logging.getLogger('disen').setLevel(logging.DEBUG)


class TestLogger(TestCase):

    # 单元测试的方法是以 "test"开头的
    def test1(self):

        logging.debug('--hi debug-')
        logging.info('--hi, info--')  # 当前等级INFO
        logging.warning('---hi, warning--')
        logging.error('---hi, error--')
        logging.critical('--hi, critical---')

    def test2(self):
        # 获取指定名称的日志记录器，并输出信息
        logger = logging.getLogger('disen')
        logger.info('--[disen]-hi, info--')
        logger.error('--[disen]-hi, error--')
        logger.critical('--[disen]-hi, critical--')

    def test3(self):
        # 设置日志的格式- formatter
        # 设置root日志记录器的格式
        # 日志格式化中常用的变量：
        #     asctime 时间
        #     name 记录器，
        #     levelname 等级名称
        #     funcName  日志输出的所在函数
        #     pathname  输出日志的所在文件的完整路径
        #     message   日志的消息

        logging.basicConfig(format='[ %(asctime)s ][ %(levelname)s]: %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',  # 设置asctime的格式
                            filename='test.log',  # 输出日志的文件名
                            filemode='a')  # 将日志的消息以追加方式写入到文件中

        logging.debug('--hi debug-')
        logging.info('--hi, info--')  # 当前等级INFO
        logging.warning('---hi, warning--')
        logging.error('---hi, error--')
        logging.critical('--hi, critical---')

    def test4(self):
        # formatter、handler、logger 之间关系?
        # handler 对象可以添加formatter
        # logger 可以添加多个 handler, 如果没有handler,默认会添加 StreamHandler

        # 常用的Handler有哪些
        #  1) StreamHandler -> 控制台打印输出的处理器
        #  2) FileHandler -> 日志文件输出的处理器
        #  3）HttpHandler  -> 网络上传日志的处理器

        logger = logging.getLogger('disen')

        # user_id 是自定义格式变量
        log_format_str = '< %(user_id)s >[ %(asctime)s ]-%(levelname)s: %(message)s'
        log_format_date = '%Y-%m-%d %H:%M:%S'

        # 实例化handler - 标准输出的
        handler1 = logging.StreamHandler()

        # 设置handler的日志等级、格式
        handler1.setLevel(logging.INFO)
        handler1.setFormatter(logging.Formatter(fmt=log_format_str, datefmt=log_format_date))

        logger.addHandler(handler1)

        handler2 = logging.FileHandler('handler.log')
        handler2.setFormatter(logging.Formatter(fmt=log_format_str,
                                                datefmt=log_format_date))
        handler2.setLevel(logging.WARN)  # 文件处理器只记录 警告信息

        logger.addHandler(handler2)

        # 创建上传日志的处理器
        # 上传日志信息中的所有信息
        httpHandler = HTTPHandler(host='10.12.155.80:5000', url='/upload_log/', method='POST')
        httpHandler.setLevel(logging.ERROR)

        logger.addHandler(httpHandler)

        # 1. 检查每个消息的等级，再判断当前日志记录器是否处理
        # 2. 在日志的记录器中 获取它的所有处理器handler
        # 3. 根据消息的等级，分别由不同的处理器处理消息。

        extra_info = {'user_id': '1000001'}

        logger.info('hi, info', extra=extra_info)
        logger.warning('hi, warning',  extra=extra_info)
        logger.error('hi, error',  extra=extra_info)
        logger.critical('hi, critical', extra=extra_info)

    def test5(self):
        # 默认的StreamHandler的Level是WARNING
        a = logging.getLogger('aaa')
        a.setLevel(logging.INFO)

        a.addHandler(logging.StreamHandler())
        a.handlers[0].setLevel(logging.INFO)

        a.info('---hi info---')
        a.warning('----hi, warning---')
        a.error('--hi, error----')
        a.critical('-hi, critical--')



