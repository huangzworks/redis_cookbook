# file: ./h/cache/string_implement.py

from redis import Redis

def set(name, value, ttl=None, client=Redis()):
    if ttl:
        client.setex(name, value, ttl)
    else:
        client.set(name, value)

def get(name, client=Redis()):
    return client.get(name)

def delete(name, client=Redis()):
    client.delete(name)
