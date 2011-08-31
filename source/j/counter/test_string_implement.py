#! /usr/bin/env python2.7

from string_implement import Counter

pv = Counter('page_view_counter')

assert( pv.get() == 0 )

assert( pv.incr() == 1 )
assert( pv.incr(5) == 6 )

assert( pv.decr() == 5 )
assert( pv.decr(3) == 2 )

pv.set(10086)
assert( pv.get() == 10086)

pv.reset()
assert( pv.get() == 0 )

print("all test OK")
