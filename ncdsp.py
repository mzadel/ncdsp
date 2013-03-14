
class ReenteredException(Exception):
    pass


vals = {}
valfuncs = {}
reading = set()


def read( valandstatetuple ):

    # guard against circular dependencies while reading
    if valandstatetuple in reading:
        raise ReenteredException("reentered!")
    reading.add(valandstatetuple)

    # compute and cache the value at this state if it hasn't been computed yet
    if valandstatetuple not in vals.keys():
        vallabel,statelabel = valandstatetuple
        vals[valandstatetuple] = valfuncs[vallabel](statelabel)

    # done reading
    reading.remove(valandstatetuple)
    return vals[valandstatetuple]


def createdelayline( name, numberofcells ):

    for i in range(1,numberofcells):
        cellname = '{0}_{1}'.format( name, i )
        # take the value of the previous cell at the previous timestep
        valfuncs[cellname] = eval( "lambda time: read( ('{0}_{1}',time-1) )".format(name,i-1) )

    # cell 0 reads from name_input at the current time
    valfuncs['{0}_0'.format(name)] = eval( "lambda time: read( ('{0}_input',time) )".format(name) )

    # name_output reads from the last cell at the current time
    valfuncs['{0}_output'.format(name)] = eval( "lambda time: read( ('{0}_{1}',time) )".format(name,numberofcells-1) )

    # fill the delay line with zeroes at time zero, except for the first cell
    # (so that it'll pull its value from name_input)
    for i in range(1,numberofcells):
        vals[( '{0}_{1}'.format(name,i), 0 )] = 0


