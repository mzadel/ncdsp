#!/usr/bin/python

#
# naivecorrectdsp.py
#


class ReenteredException(Exception):
    pass

vals = {}
determinefuncs = {}

class Value:
    def __init__(self, vallabel, statelabel, determinefunc):

        self.vallabel = vallabel
        self.statelabel = statelabel
        self.hasbeenentered = False

        # add me to the global hashes of labeled vals
        if self.vallabel not in vals.keys():
            # add an initial state dict for this value if it doesn't exist
            vals[self.vallabel] = {}
        vals[vallabel][statelabel] = self

        # add my determinefunc to 
        determinefuncs[self.vallabel] = determinefunc

    def read(self):

        if self.hasbeenentered:
            raise ReenteredException("reentered!")
        self.hasbeenentered = True

        # determine my value at this state if it's not cached
        if not state in self.knownvalues.keys():
            self.knownvalues[state] = self.determinefunc(state)

        self.hasbeenentered = False
        return self.knownvalues[state]




# circular delay line
'cella' = Value( lambda time: vals['celle'].read(time-1) )
'cellb' = Value( lambda time: vals['cella'].read(time-1) )
'cellc' = Value( lambda time: vals['cellb'].read(time-1) )
'celld' = Value( lambda time: vals['cellc'].read(time-1) )
'celle' = Value( lambda time: vals['celld'].read(time-1) )


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
