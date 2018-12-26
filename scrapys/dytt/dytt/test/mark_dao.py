from dao.base import BaseDao
from models.mark import Mark

dao = BaseDao(None)

dao.save(Mark('19991', 'hao123', 'http://hao123.com', 'baidu'))
