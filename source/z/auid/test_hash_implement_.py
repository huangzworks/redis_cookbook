#! /usr/bin/env python2.7

from redis import Redis
r = Redis()
r.flushdb()

from hash_implement import *

user_id = Auid('user_id')

assert( user_id.get() == 0 )

assert( user_id.incr() == 1 )
assert( user_id.incr() == 2 )

assert( user_id.get() == 2 )

print("all test OK")
