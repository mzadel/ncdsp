#!/usr/bin/python

from ncdsp import *


# -(feedforward)--------------------------------------------

# feedforward comb filter
# see https://ccrma.stanford.edu/~jos/pasp/Feedforward_Comb_Filters.html
# defines name_out value for output
# depends on external definition of name_in, from which it takes its input
def feedforwardcomb( name, b0, bM, M ):
    y = name+'_out'
    x = name+'_in'
    valfuncs[y] = lambda n: b0 * read((x,n)) + bM * read((x,n-M))

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

# feedback comb filter
# see https://ccrma.stanford.edu/~jos/pasp/Feedback_Comb_Filters.html
# defines name_out value for output
# depends on external definition of name_in, from which it takes its input
# NB: assumes name_out is set to zero for time < 0 (to provide base cases for
# the the recurrence in y)
def feedbackcomb( name, b0, aM, M ):
    y = name+'_out'
    x = name+'_in'
    valfuncs[y] = lambda n: b0 * read((x,n)) - aM * read((y,n-M)) if n>=0 else 0

feedbackcomb('fbc', 0.8, 0.1, 10 )

# input: impulse at time 0, zeroes everywhere else
valfuncs['fbc_in'] = lambda time: 1 if time == 0 else 0

print 'feedback'
for t in range(50):
    print t, 'fbc_in', read(('fbc_in',t)), 'fbc_out', read(('fbc_out',t))


# vim:sw=4:ts=4:ai:et
