# coding:utf-8

# file: ./r/log/list_implement.py

from redis import Redis

# Redis列表的边界下标
LEFTMOST = 0
RIGHTMOST = -1

class Log:
    
    def __init__(self, name, client=Redis()):
        self.name = name
        self.client = client

    def append(self, content):
        return self.client.lpush(self.name, content)

    def read(self, start=LEFTMOST, stop=RIGHTMOST):
        return self.client.lrange(self.name, start, stop)

    def length(self):
        return self.client.llen(self.name)

    def clear(self):
        # 因为del是Python的保留字
        # 所以redis-py用delete代替del命令
        self.client.delete(self.name)

    def keep(self, size):
        # 只保留log[0:size-1]范围内的条目
        self.client.ltrim(self.name, LEFTMOST, size-1)
