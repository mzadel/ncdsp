
from ncdsp import *


# createdelayline() creates a delay line, implemented as a 'bucket brigade' of
# cells.  This mimics how a delay line is typically laid out in memory.
#
# Each cell passes its value to the next cell in the chain at each timestep.
#
# You supply the delay line name as an argument.  The value 'name_lastcell' is
# an alias for the last cell in the chain.
#
# You additionally have to define a value called 'name_firstcell', which the
# first cell in the chain takes its value from.

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

    # cell 0 reads from name_firstcell at the current time
    connect( (name,0), name+'_firstcell' )

    # name_lastcell reads from the last cell at the current time
    connect( name+'_lastcell', (name,numberofcells-1) )

    # fill the delay line with zeroes at time zero, except for the first cell
    # (so that it'll pull its value from name_firstcell)
    for i in range(1,numberofcells):
        vals[( '{0}_{1}'.format(name,i), 0 )] = 0


# an alternative way to do a delay is to take inspiration from a difference
# equation formulation:
#  valfuncs['y'] = lambda time: read(('x',time-10))
# for a 10-sample delay.  The catch with this is that you have to ensure that
# ('x',time-10) exists.


# shorthard for connecting y to x, ie:
# y <- x
# or y[n] = x[n]
def connect( y, x ):
    valfuncs[y] = lambda state: read((x,state))


# feedforward comb filter
# see https://ccrma.stanford.edu/~jos/pasp/Feedforward_Comb_Filters.html
# defines name_out value for output
# depends on external definition of name_in, from which it takes its input
def feedforwardcomb( name, b0, bM, M ):
    y = name+'_out'
    x = name+'_in'
    valfuncs[y] = lambda n: b0 * read((x,n)) + bM * read((x,n-M))


# feedback comb filter
# see https://ccrma.stanford.edu/~jos/pasp/Feedback_Comb_Filters.html
# defines name_out value for output
# depends on external definition of name_in, from which it takes its input
# NB: assumes name_out is set to zero for time < 0 (to provide base cases for
# the the recurrence in y)
def feedbackcomb( name, b0, aM, M ):
    y = name+'_out'
    x = name+'_in'
    valfuncs[y] = lambda n: b0 * read((x,n)) - aM * read((y,n-M)) if n>=0 else 0


# vim:sw=4:ts=4:ai:et
