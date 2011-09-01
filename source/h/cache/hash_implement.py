# file: ./h/cache/hash_implement.py

from redis import Redis

def set(category, name, value, client=Redis()):
    client.hset(category, name, value)

def get(category, name, client=Redis()):
    return client.hget(category, name)

def delete(category, name, client=Redis()):
    client.hdel(category, name)

def expire(category, ttl, client=Redis()):
    client.expire(category, ttl)

def ttl(category, client=Redis()):
    return client.ttl(category)

def size(category, client=Redis()):
    return client.hlen(category)


# test:
if __name__ == "__main__":

    from time import sleep

    category = 'greet'
    key = 'morning'
    value = 'good morning!'
    expire_time = 3

    set(category, key, value)
    assert get(category, key) == value
    assert size(category) == 1

    delete(category, key)
    assert get(category, key) == None
    assert size(category) == 0

    set(category, key,value)
    expire(category, expire_time)
    assert ttl(category) != None

    sleep(expire_time * 2)
    assert get(category, key) == None
