# coding:utf-8

# file: ./j/counter/string_implement.py

from redis import Redis

INITIAL_VALUE = 0

class Counter:
    
    def __init__(self, name, client=Redis()):
        self.name = name
        self.client = client

    def incr(self, increment=1):
        # redis-py 用 incr 代替 incrby，所以可以指定增量
        value = self.client.incr(self.name, increment)
        return int(value)

    def decr(self, decrement=1):
        # redis-py 用 decr 代替 decrby，所以可以指定减量
        value = self.client.decr(self.name, decrement)
        return int(value)

    def set(self, value):
        self.client.set(self.name, value)

    def get(self):
        value = self.client.get(self.name)
        return INITIAL_VALUE if value is None else int(value)

    def reset(self):
        self.set(INITIAL_VALUE)
