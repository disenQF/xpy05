import sys

from dao.base import BaseDao
from models.proxy_id import ProxyId

dao = BaseDao()

dao.save(ProxyId('HTTP', '10.12.155.80', 8888))
