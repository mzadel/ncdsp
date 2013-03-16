
from ncdsp import *

def createdelayline( name, numberofcells ):

    for i in range(1,numberofcells):
        # labels for each cell are (name,cellnum) tuples
        # each cell gets the value of the previous cell at the previous timestep

        # define the valfuncs for each of the cells.
        # problem: if we just pass in name and i into a lambda, they'll refer
        # to the variables in the closure, which'll be the last values they
        # were set to in the loop.
        # instead, makefunc() returns the lambda we need.  we supply the name
        # and i as parameter defaults.  from piro on stack overflow:
        # "parameter defaults are evaluated when the def statement is executed,
        # and thus the value of the loop variable is frozen"
        def makefunc( name=name, i=i ):
            return lambda time: read( ( ( name, i-1 ), time-1 ) )
        valfuncs[(name,i)] = makefunc(name,i)

    # cell 0 reads from name_input at the current time
    valfuncs[(name,0)] = lambda time: read( (name+'_input',time) )

    # name_output reads from the last cell at the current time
    valfuncs[name+'_output'] = lambda time: read( ((name,numberofcells-1),time) )

    # fill the delay line with zeroes at time zero, except for the first cell
    # (so that it'll pull its value from name_input)
    for i in range(1,numberofcells):
        vals[( '{0}_{1}'.format(name,i), 0 )] = 0

