
class ReenteredRead(Exception):
    pass


vals = {}
valfuncs = {}
reading = set()


# the core function: read() -- reads a value from the environment
#  if the value has been computed before, it returns the cached value
#  if it hasn't, compute the value, cache it, and return the value
# read() does error checking for circular dependencies and for values not found
# in the environment.
# without the error checking, the basic structure is simply this:
#  if (vallabel,statelabel) not in vals.keys():
#      vals[(vallabel,statelabel)] = valfuncs[vallabel](statelabel)
#  return vals[(vallabel,statelabel)]

def read( valandstatetuple ):

    # guard against circular dependencies while reading
    if valandstatetuple in reading:
        raise ReenteredRead('reentered while reading key {0}'.format(repr(valandstatetuple)))
    reading.add(valandstatetuple)

    # compute and cache the value at this state if it hasn't been computed yet
    if valandstatetuple not in vals.keys():
        vallabel,statelabel = valandstatetuple
        try:
            vals[valandstatetuple] = valfuncs[vallabel](statelabel)
        except KeyError:
            print 'read(): KeyError while trying to read value with label', valandstatetuple
            raise

    # done reading
    reading.remove(valandstatetuple)
    return vals[valandstatetuple]

# vim:sw=4:ts=4:ai:et
