#!/usr/bin/python

#
# ncdsp_circulardependency.py
#

# test that the circular dependency checking works

from ncdsp import *

determinefuncs['cella'] = lambda time: read( ('cellb',time) )
determinefuncs['cellb'] = lambda time: read( ('cella',time) )

vals[('cella',0)] = 0
vals[('cellb',0)] = 1

read( ('cella', 15) )
read( ('cellb', 15) )
# should trip an exception

# vim:sw=4:ts=4:ai:et
