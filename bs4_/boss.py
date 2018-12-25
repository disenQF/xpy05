"""
Boss直聘
城市信息
    -> https://www.zhipin.com/common/data/city.json

所有岗位
    -> https://www.zhipin.com/job_detail/?ka=header-job

搜索接口：
    https://www.zhipin.com/job_detail/?query=python&scity=101110100

   下一页：
    https://www.zhipin.com/job_detail/?query=python&scity=101110100&page=2
"""


def download(url, callback):
    pass


def parse_city(resp):
    pass


def parse_job(resp):
    pass


def start_spider():
    pass


def item_pipeline(**data):
    print(data)


if __name__ == '__main__':
    start_spider()