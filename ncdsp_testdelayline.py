#!/usr/bin/python

#
# ncdsp_testdelayline.py
#

import sys

from ncdsphelpers import *
from ncdsp import *

# create the delay line
createdelayline( 'yummy', 40 )

# set up the input
# always return 0, unless it's the first timestep
# introduce an impulse at the first timestep
valfuncs['yummy_input'] = lambda state: 0
vals[('yummy_input',0)] = 1
vals[('yummy_input',7)] = 5

for time in range(50):

    # print the input value
    print 'yummy_input:', read(('yummy_input',time)), '         ' ,

    # print the delay line contents for this timestep
    for cellnum in range( 40 ):
        cellvalue = read((('yummy',cellnum),time))
        sys.stdout.write(repr(cellvalue))

    # print the output value
    print '          yummy_output:', read(('yummy_output',time))


# vim:sw=4:ts=4:ai:et
