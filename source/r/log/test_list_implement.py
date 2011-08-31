#! /usr/bin/env python2.7

from list_implement import *

log = Log('system_log')

log.append('power on')
log.append('user login')

assert(log.length() == 2)
assert(log.read() == ['user login', 'power on'])

log.append('3')
log.append('2')
log.append('1')

log.keep(3)
assert(log.length() == 3)
assert(log.read() == ['1', '2', '3'])

log.clear()
assert(log.length() == 0)

print("all test OK")
