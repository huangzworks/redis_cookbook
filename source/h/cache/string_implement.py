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


# test:
if __name__ == "__main__":

    from time import sleep

    key = 'phone'
    value = '10086'
    expire_time = 3

    set(key, value)
    assert get(key) == value 

    delete(key)
    assert get(key) == None 

    set(key, value, expire_time)
    assert get(key) == value 

    sleep(expire_time * 2)
    assert get(key) == None 
