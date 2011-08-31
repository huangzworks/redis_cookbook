# coding: utf-8

# file: ./s/timeline/sorted_set_implement.py

from redis import Redis
from time import time

# Redis有序集边界
LEFTMOST = 0
RIGHTMOST = -1

class Timeline:

    def __init__(self, name, client=Redis()):
        self.name = name
        self.client = client

    def append(self, content):
        # time()函数生成当前时间的unixtime值
        self.client.zadd(self.name, score=time(), value=content)

    def range(self, start=LEFTMOST, stop=RIGHTMOST, display_time=False):
        # 使用zrevrange命令，读出最新的数据
        return self.client.zrevrange(self.name, start, stop, withscores=display_time)

    def range_between_time(self, min, max, display_time=False):
        # min和max也必须是unixtime值
        # 注意zrevrangebyscore命令参数的摆放是max先而min后
        return self.client.zrevrangebyscore(self.name, max, min, withscores=display_time)

    def delete(self, content):
        return self.client.zrem(self.name, content)

    def delete_between_time(self, min, max):
        # min和max也必须是unixtime值
        return self.client.zremrangebyscore(self.name, min=min, max=max)

    def length(self):
        return self.client.zcard(self.name)
