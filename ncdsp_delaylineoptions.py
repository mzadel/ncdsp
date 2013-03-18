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

xs = [ read(('x',n)) for n in range(40) ]
print xs
ys = [ read(('y',n)) for n in range(40) ]
print ys

# then bucket brigade
# then an implementation where the values stay in-place

# -(bucket brigade)-----------------------------------------

vals.clear()
valfuncs.clear()

valfuncs['x'] = lambda time: 1.0 if time==0 else 0.0

valfuncs[('delay',0)] = lambda time: read(('x',time))
valfuncs[('delay',1)] = lambda time: read((('delay',0),time-1))
valfuncs[('delay',2)] = lambda time: read((('delay',1),time-1))
valfuncs[('delay',3)] = lambda time: read((('delay',2),time-1))
valfuncs[('delay',4)] = lambda time: read((('delay',3),time-1))

valfuncs['y'] = lambda time: read((('delay',4),time))

xs = [ read(('x',n)) for n in range(40) ]
print xs
ys = [ read(('y',n)) for n in range(40) ]
print ys

# so with this setup, there's only a delay of 4, even with 5 cells of delay
# either the read or the write have to introduce an extra tick of delay



# vim:sw=4:ts=4:et:ai
