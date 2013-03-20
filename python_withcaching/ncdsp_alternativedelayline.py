#!/usr/bin/python

#
# ncdsp_alternativedelayline.py
#
# make a delay line just by referring the past
# the only trick is that you have to make sure the value you're delaying is
# defined before time 0
#

from ncdsp import *

# set up the original number we're going to delay
# for the sake of demonstration the value of orig before time 0 is going to be
# 2, and the value of orig at and after time 0 is going to 0
# (typically, though, the value of orig before time 0 would be zero)
for t in range(0,100):
    vals[('orig',t)] = 0
for t in range(-40,0):
    vals[('orig',t)] = 2

# you could also do something like
#  valfuncs['orig'] = lambda t: 0 if t>=0 else 2
# but the above example spells out what samples are strictly necessary to be
# defined before time 0

# introduce a couple of impulses
vals[('orig',0)] = 1
vals[('orig',7)] = 5

# set up the function to determine the delayed version
valfuncs['delayed'] = lambda time: read( ('orig',time-40) )

for time in range(50):

    # print timestep
    print 't{0:2}     '.format( time ),

    # print the first cell's value
    print 'orig:', read(('orig',time)), '     ' ,

    # print the last cell's value
    print 'delayed:', read(('delayed',time))


# vim:sw=4:ts=4:ai:et
