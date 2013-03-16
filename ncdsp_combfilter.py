#!/usr/bin/python

from ncdsp import *
from ncdsphelpers import feedforwardcomb, feedbackcomb


# -(feedforward)--------------------------------------------

feedforwardcomb('ffc', 1, 0.5, 10 )

# input: impulse at time 0, zeroes everywhere else
valfuncs['ffc_in'] = lambda time: 1 if time == 0 else 0

print 'feedforward'
for t in range(50):
    print t, 'ffc_in', read(('ffc_in',t)), 'ffc_out', read(('ffc_out',t))



# -(feedback)-----------------------------------------------

# clear out the previous state
vals.clear()
valfuncs.clear()

feedbackcomb('fbc', 0.8, 0.1, 10 )

# input: impulse at time 0, zeroes everywhere else
valfuncs['fbc_in'] = lambda time: 1 if time == 0 else 0

print 'feedback'
for t in range(50):
    print t, 'fbc_in', read(('fbc_in',t)), 'fbc_out', read(('fbc_out',t))


# vim:sw=4:ts=4:ai:et
