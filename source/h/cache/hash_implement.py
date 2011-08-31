# file: ./h/cache/hash_implement.py

from redis import Redis

class Cache:
    
    def __init__(self, category, client=Redis()):
        self.category = category
        self.client = client

    def set(self, name, value):
        self.client.hset(self.category, name, value)

    def get(self, name):
        return self.client.hget(self.category, name)

    def expire(self, ttl):
        self.client.expire(self.category, ttl)

    def ttl(self):
        return self.client.ttl(self.category)

    def size(self):
        return self.client.hlen(self.category)
