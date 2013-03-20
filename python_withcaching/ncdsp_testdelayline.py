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
valfuncs['yummy_firstcell'] = lambda state: 0
vals[('yummy_firstcell',0)] = 1
vals[('yummy_firstcell',7)] = 5

for time in range(50):

    # print the first cell's value
    print 'yummy_firstcell:', read(('yummy_firstcell',time)), '         ' ,

    # print the delay line contents for this timestep
    for cellnum in range( 40 ):
        cellvalue = read((('yummy',cellnum),time))
        sys.stdout.write(repr(cellvalue))

    # print the last cell's value
    print '          yummy_lastcell:', read(('yummy_lastcell',time))


# vim:sw=4:ts=4:ai:et
