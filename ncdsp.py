
class ReenteredRead(Exception):
    pass


vals = {}
valfuncs = {}
reading = set()


def read( valandstatetuple ):

    # guard against circular dependencies while reading
    if valandstatetuple in reading:
        raise ReenteredRead("reentered!")
    reading.add(valandstatetuple)

    # compute and cache the value at this state if it hasn't been computed yet
    if valandstatetuple not in vals.keys():
        vallabel,statelabel = valandstatetuple
        vals[valandstatetuple] = valfuncs[vallabel](statelabel)

    # done reading
    reading.remove(valandstatetuple)
    return vals[valandstatetuple]

# vim:sw=4:ts=4:ai:et
