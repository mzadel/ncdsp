#!/usr/bin/python

# karplusstrong.py
#
# this is a bit harder to read, but it's much faster than the haskell version
# since it uses memoization

from ncdsp import *
from ncdsphelpers import connect

valfuncs['excitation'] = lambda n: 1.0 if n == 0 else 0.0

valfuncs['output'] = lambda n: read(('excitation',n)) + read(('filteroutput',n))

connect('delayinput','output' )
delaysamples = 50
valfuncs['delayoutput'] = lambda n: read(('delayinput',n-delaysamples))

connect('filterinput','delayoutput')
valfuncs['filteroutput'] = lambda n: 0.5*read(('filterinput',n)) + 0.5*read(('filteroutput',n-1)) if n>=0 else 0.0

for n in range(2000):
    print read(('output',n))

# vim:sw=4:ts=4:et:ai:
