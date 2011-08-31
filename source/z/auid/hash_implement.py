# file: ./z/auid/hash_implement.py

from redis import Redis

INITIA_VALUE = 0
INCREMENT = 1
KEY = 'auid'

class Auid:

    def __init__(self, name, client=Redis(), key=KEY):
        self.key = key
        self.name = name
        self.client = client

    def incr(self):
        value = self.client.hincrby(self.key, self.name, INCREMENT)
        return int(value)

    def get(self):
        value = self.client.hget(self.key, self.name)
        return INITIA_VALUE if value is None else int(value)
