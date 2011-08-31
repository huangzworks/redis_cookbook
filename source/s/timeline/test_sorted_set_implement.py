#! /usr/bin/env python2.7
# coding: utf-8

from sorted_set_implement import Timeline
from time import time, sleep

t = Timeline('time_and_date')

t.append('good morning')
sleep(1)
t.append('having breakfast')
sleep(1)
t.append('go to sleep')
sleep(1)

assert( t.length() == 3 )
assert( t.range() == \
        ['go to sleep', 'having breakfast', 'good morning'] )

assert( t.range_between_time(0, time()) == \
        ['go to sleep', 'having breakfast', 'good morning'] )

t.delete('go to sleep')

assert( t.length() == 2)
assert( t.range() == \
        ['having breakfast', 'good morning'] )

t.delete_between_time(0, time())
assert( t.length() == 0 )

print("all test OK")
