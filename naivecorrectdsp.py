#!/usr/bin/python

#
# naivecorrectdsp.py
#


class ReenteredException(Exception):
    pass

vals = {}

class Value:
    def __init__(self,determinefunc):
        self.determinefunc = determinefunc
        self.hasbeenentered = False
        self.knownvalues = {}

    def read(self,state):

        if self.hasbeenentered:
            raise ReenteredException("reentered!")
        self.hasbeenentered = True

        # determine my value at this state if it's not cached
        if not state in self.knownvalues.keys():
            self.knownvalues[state] = self.determinefunc(state)

        self.hasbeenentered = False
        return self.knownvalues[state]



# circular delay line
vals['cella'] = Value( lambda time: vals['celle'].read(time-1) )
vals['cellb'] = Value( lambda time: vals['cella'].read(time-1) )
vals['cellc'] = Value( lambda time: vals['cellb'].read(time-1) )
vals['celld'] = Value( lambda time: vals['cellc'].read(time-1) )
vals['celle'] = Value( lambda time: vals['celld'].read(time-1) )


# values at the initial time:
vals['cella'].knownvalues[0] = 0
vals['cellb'].knownvalues[0] = 1
vals['cellc'].knownvalues[0] = 0
vals['celld'].knownvalues[0] = 0
vals['celle'].knownvalues[0] = 0



# determine the values at the end
vals['cella'].read(15)
vals['cellb'].read(15)
vals['cellc'].read(15)
vals['celld'].read(15)
vals['celle'].read(15)












# vim:sw=4:ts=4:ai:et
