#!/usr/bin/python

#
# naivecorrectdsp.py
#

# the idea behind this is to make it easier to reason about dsp code
# each value at each timestep is kept in a global table indexed by (valuelabel,statelabel)
# read((valuelabel,statelabel)) returns the appropriate value, cacheing the value as necessary
# it raises an exception if you try to recursively read a given value (which
# means there's circular dependency)

# once you populate all the values, you can print the sequences so that you
# have a reference to compare against when you're implementing a more efficient
# version of the algorithm

# this approach should make it easier to implement a set of time-domain
# recurrence functions, or a system block diagram

# there's a danger that you'll get a stack overflow if you don't have a base
# case for the recursion back through time, so you have to ensure that you have
# that in place

from ncdsp import *

# setup the internal functions that are used to update each value
# circular delay line
valfuncs['cella'] = lambda time: read( ('celle', time-1 ) )
valfuncs['cellb'] = lambda time: read( ('cella', time-1 ) )
valfuncs['cellc'] = lambda time: read( ('cellb', time-1 ) )
valfuncs['celld'] = lambda time: read( ('cellc', time-1 ) )
valfuncs['celle'] = lambda time: read( ('celld', time-1 ) )

# initial values
vals[('cella',0)] = 0
vals[('cellb',0)] = 1
vals[('cellc',0)] = 0
vals[('celld',0)] = 0
vals[('celle',0)] = 0

# determine the values at the end
# read at the final times.  this should populate all the cells at all timesteps
# then print out the values
read( ('cella', 15) )
read( ('cellb', 15) )
read( ('cellc', 15) )
read( ('celld', 15) )
read( ('celle', 15) )
for i in range(16):
    print vals[('cella',i)], vals[('cellb',i)], vals[('cellc',i)], vals[('celld',i)], vals[('celle',i)]

print "alternatively, compute one at a time:"
for i in range(16):
    print read(('cella',i)), read(('cellb',i)), read(('cellc',i)), read(('celld',i)), read(('celle',i))

# vim:sw=4:ts=4:ai:et
