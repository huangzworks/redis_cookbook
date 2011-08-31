# file: ./z/auid/string_implement.py

from redis import Redis

INITIAL_VALUE = 0

class Auid:
    
    def __init__(self, name, client=Redis()):
        self.name = name
        self.client = client

    def incr(self):
        value = self.client.incr(self.name)
        return int(value)

    def get(self):
        value = self.client.get(self.name)
        return INITIAL_VALUE if value is None else int(value)
