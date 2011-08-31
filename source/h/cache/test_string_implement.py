#! /usr/bin/env python2.7

from string_implement import *
from time import sleep

name = 'page_cache'
value = 'balh balh ...'
ttl = 5

# set

set(name, value)
assert( get(name) == value )

# set with ttl 
set(name, value, ttl)
assert( get(name) == value )

sleep(ttl+1)
assert( get(name) == None )

# delete
set(name, value)
delete(name)
assert( get(name) == None )

print("all test OK")
