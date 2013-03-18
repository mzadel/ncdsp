#!/usr/bin/python

#
# ncdsp_delaylineoptions.py
#

M = 5

vals = {}
valfuncs = {}

def read( label ):
    if label not in vals.keys():
        vallabel, statelabel = label
        vals[label] = valfuncs[vallabel](statelabel)
    return vals[label]

valfuncs['x'] = lambda time: 1.0 if time==0 else 0.0
valfuncs['y'] = lambda time: read(('x',time-M))

l = [ read(('y',n)) for n in range(40) ]
print l




# vim:sw=4:ts=4:et:ai
