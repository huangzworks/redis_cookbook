# file: ./j/counter/hash_implement.py

from redis import Redis

INITIALI_VALUE = 0
KEY = 'counter'

class Counter:
    
    def __init__(self, field, client=Redis(), key=KEY):
        self.key = key
        self.field = field
        self.client = client

    def incr(self, increment=1):
        value = self.client.hincrby(self.key, self.field, increment)
        return int(value)

    def decr(self, decrement=1):
        value = self.client.hincrby(self.key, self.field, 0-decrement)
        return int(value)

    def set(self, value):
        self.client.hset(self.key, self.field, value)

    def get(self):
        value = self.client.hget(self.key, self.field)
        return INITIALI_VALUE if value is None else int(value)

    def reset(self):
        self.set(INITIALI_VALUE)
