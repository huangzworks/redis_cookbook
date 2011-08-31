#! /usr/bin/env python2.7

from hash_implement import *
from time import sleep

page = Cache('page_cache')

# set
page.set('/topic/123', 'hello')
page.set('/topic/10086', 'moto')

# size
assert(page.size() == 2)

# get
assert(page.get('/topic/123') == 'hello')
assert(page.get('/topic/10086') == 'moto')

# ttl & expire
assert(page.ttl() == None)

page.expire(3)
assert(page.ttl() != None)
sleep(5)
assert(page.size() == 0)  


print("all test OK")
