#!/usr/bin/python

#
# ncdsp_circulardependency.py
#

# test that the circular dependency checking works

class ReenteredException(Exception):
    pass

vals = {}
determinefuncs = {}
reading = set()

def read( valandstatetuple ):

    # guard against circular dependencies while reading
    if valandstatetuple in reading:
        raise ReenteredException("reentered!")
    reading.add(valandstatetuple)

    # compute and cache the value at this state if it hasn't been computed yet
    if valandstatetuple not in vals.keys():
        vallabel,statelabel = valandstatetuple
        vals[valandstatetuple] = determinefuncs[vallabel](statelabel)

    # done reading
    reading.remove(valandstatetuple)
    return vals[valandstatetuple]


determinefuncs['cella'] = lambda time: read( ('cellb',time) )
determinefuncs['cellb'] = lambda time: read( ('cella',time) )

vals[('cella',0)] = 0
vals[('cellb',0)] = 1

read( ('cella', 15) )
read( ('cellb', 15) )
# should trip an exception

# vim:sw=4:ts=4:ai:et
