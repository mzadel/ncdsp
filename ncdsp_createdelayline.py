#!/usr/bin/python

#
# ncdsp_createdelayline.py
#

import sys

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

# automatically create a delay line
def createdelayline( name, numberofcells ):

    for i in range(1,numberofcells):
        cellname = '{0}_{1}'.format( name, i )
        # take the value of the previous cell at the previous timestep
        determinefuncs[cellname] = eval( "lambda time: read( ('{0}_{1}',time-1) )".format(name,i-1) )

    # cell 0 reads from name_input at the current time
    determinefuncs['{0}_0'.format(name)] = eval( "lambda time: read( ('{0}_input',time) )".format(name) )

    # name_output reads from the last cell at the current time
    determinefuncs['{0}_output'.format(name)] = eval( "lambda time: read( ('{0}_{1}',time) )".format(name,numberofcells-1) )

    # fill the delay line with zeroes at time zero
    for i in range(numberofcells):
        vals[( '{0}_{1}'.format(name,i), 0 )] = 0


# create the delay line
createdelayline( 'yummy', 4 )

# set up the input
# always return 0, unless it's the first timestep
# introduce an impulse at the first timestep
determinefuncs['yummy_input'] = lambda state: 0
vals[('yummy_input',0)] = 1

#print determinefuncs.keys()
#print
#print vals.keys()
#print


print 'before loop'
for time in range(15):
    print 'time', time
    for cell in range( 4 ):
        print 'cell', cell
        cellname = 'yummy_{0}'.format(cell)
        sys.stdout.write(chr(read((cellname,time))))
    sys.stdout.write("\n")





















# vim:sw=4:ts=4:ai:et
