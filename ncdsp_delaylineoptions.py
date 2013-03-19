#!/usr/bin/python

#
# ncdsp_delaylineoptions.py
#

vals = {}
valfuncs = {}

def read( label ):
    if label not in vals.keys():
        vallabel, statelabel = label
        vals[label] = valfuncs[vallabel](statelabel)
    return vals[label]

valfuncs['x'] = lambda time: 1.0 if time==0 else 0.0
valfuncs['y'] = lambda time: read(('x',time-5))

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

# delay line.  NB, we introduce an extra step of delay in the first cell
# there would be only a delay of 4, even with 5 cells of delay, without that
# (either the read or the write have to introduce an extra tick of delay)
valfuncs[('delay',0)] = lambda time: read(('x',time-1))
valfuncs[('delay',1)] = lambda time: read((('delay',0),time-1))
valfuncs[('delay',2)] = lambda time: read((('delay',1),time-1))
valfuncs[('delay',3)] = lambda time: read((('delay',2),time-1))
valfuncs[('delay',4)] = lambda time: read((('delay',3),time-1))

valfuncs['y'] = lambda time: read((('delay',4),time))

xs = [ read(('x',n)) for n in range(40) ]
print xs
ys = [ read(('y',n)) for n in range(40) ]
print ys


# -(pointer delay line)-------------------------------------

vals.clear()
valfuncs.clear()

valfuncs['pointer'] = lambda n: n % 5

valfuncs['x'] = lambda time: 1.0 if time==0 else 0.0

valfuncs[('delay',0)] = lambda n: read((('delay',0),n-1)) if read(('pointer',n))!=0 else read(('x',n))
valfuncs[('delay',1)] = lambda n: read((('delay',1),n-1)) if read(('pointer',n))!=1 else read(('x',n))
valfuncs[('delay',2)] = lambda n: read((('delay',2),n-1)) if read(('pointer',n))!=2 else read(('x',n))
valfuncs[('delay',3)] = lambda n: read((('delay',3),n-1)) if read(('pointer',n))!=3 else read(('x',n))
valfuncs[('delay',4)] = lambda n: read((('delay',4),n-1)) if read(('pointer',n))!=4 else read(('x',n))

# read from the existing value of a cell as you go into the timestep, *before*
# overwriting the cell
valfuncs['y'] = lambda n: read((('delay',read(('pointer',n))),n-1))

print 'the pointer version'

xs = [ read(('x',n)) for n in range(40) ]
print xs
ys = [ read(('y',n)) for n in range(40) ]
print ys

# maybe do this where you go: compute these cells for this timestep
# and make it stateful, in the way that it would be in matlab or whatever
# and then you can just throw and exception if the timesteps are done out of order
# it might be easier to write (the above is a little unituitive, I think...)


# vim:sw=4:ts=4:et:ai
