
# NCDSP

"naive (but correct) digital signal processing"

DSP implementations can be hard to translate into efficient code, espcially if
you're just learning signal processing for the first time.  What order should I
do these operations in?  When do I increment the pointer?  This array has to be
*how* big again?  The point of the examples given in this project is to
demonstrate ways to create high-level implementations of DSP algorithms that
can serve as references for more optimized implementations.

Instead of having to mess around with pointer arithmetic and implementation
details, the idea is to do it first in a non-real-time, naive, but correct way.
Using that code, you can generate correct input and output examples to compare
subsequent, more efficient implementations against.

Basically the strategy taken here is to start from DSP block diagrams and
difference equations (aka recurrence relations), and translate those into code
that closely resembles those difference equations.  In our examples, the state
of the world at each timestep is generated functionally and recursively from
previous states, and there is no dependency on global variables.

There are two implementations of this idea here, one in Python and one in
Haskell.

## Python version

Say we want to implement a simple five-sample delay, corresponding to the
following difference equation:

    y(n) = x(n-5)

We could implement this functionally in Python as follows:

    def y(n): return x(n-5)

We could then define the values of x at all timesteps:

    def x(n): return 1.0 if n==0 else 0.0

which means that x(n) is 1.0 at time 0, and 0.0 the rest of the time.  This is
a simple impulse at time zero.

To evaluate this, we would just call y() to determine the value of the output
at each timestep.  We could do it this way:

    for n in range(40):
        print y(n)

or we could use a list comprehension to collect the values into a list:

    print [ y(n) for n in range(40) ]

We see that we have a delay of five samples.

The important point here, though, is that the function that gives the values
for each variable only calls other functions that give the value of variables,
which get called recursively down to some base case (here, the definition of
x(n)).  That way, we can think mathematically, and each variable's value is
determined purely from the mathematical equations and not some global variable
that's being mutated in a loop (which can be tricky to think about in a lot of
cases).

### Dumping out the reference data

Here's an example of setting up some input, and then dumping out the
input/output pair for later comparison.

    def x(n):
        if n==0: return 1.0
        if n==1: return 6.0
        if n==3: return 3.0
        if n==4: return 7.0
        return 0.0

    # this is the algorithm we're interested in: a 5-sample delay
    def y(n): return x(n-5)

    xs = [ x(n) for n in range(40) ]
    ys = [ y(n) for n in range(40) ]

    print xs
    print ys

This prints out two lists: one for what the value of x() is at each timestep
starting at zero (ie, the input), and one for the value of what y() is at each
timestep.  We get

    [1.0, 6.0, 0.0, 3.0, 7.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 6.0, 0.0, 3.0, 7.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

Then we can save those lists in a text file, and when we implement a more
efficient delay routine, we can give it this input (the first list), and see if
its output matches our reference implementation's output (the second list).

## Fancier Python version

One thing we might run into with the previous approach is that if we try to
drill down back from a time far into the future, we'll blow our stack because
of the recursion.  Say you ask for y() at time n=1000000, it might have to call
a million or more functions to determine what that value is.

I've made an alternative version here that caches a given variable's value at a
given time when you ask for it.  Subsequent reads will use the variable's
cached value instead of recursing through the functions to re-determine its
value.  (That is, I'm 'memoizing' the functions.)

The variable values are kept in a Python dictionary called vals.  Variable
values at a given timestep are referred to using a 2-tuple containing the
variable's name and the timestep.  ('x',100) would refer to the value of the
variable x at timestep n=100.

    vals[('x',100)] = 1.0       # cache the value for 'x' and timestep 100

The function that describes how to evaluate a variable at a given timestep is
defined like so:

    valfuncs['x'] = lambda time: 1.0 if time==0 else 0.0

Finally, to read a given variable's value at a given timestep, you use the read() function:

    valfuncs['y'] = lambda time: read(('x',time-5))

valfuncs here is a dictionary that maps variable names to anonymous functions
(ie lambdas) that describe how to derive them

read() basically just checks if there's a cached value for what you're trying
to read, and if it's not there, computes the value by calling the appropriate
function.  It's more or less just this:

    def read( label ):
        if label not in vals.keys():
            vallabel, statelabel = label
            vals[label] = valfuncs[vallabel](statelabel)
        return vals[label]

(The actual read() function also checks whether you've created a circular
dependency between your variable functions, which would of course never
return.)

So if you wanted to do what we did above (a 5-sample delay), you'd formulate it
as follows:

    from ncdsp import *
    valfuncs['x'] = lambda time: 1.0 if time==0 else 0.0
    valfuncs['y'] = lambda time: read(('x',time-5))
    for n in range(40):
        print read(('y',n))

One advantage of doing it this way is that you are caching values at various
times in the simulation, which can avoid re-computing values.  Also, since the
function names are being resolved at runtime, you can be fancier about what
kinds of relationships you build with this scheme.  You can see some ways of
doing that in the examples.



## Haskell version

Haskell is a really nice functional language whose syntax lends itself to
thinking mathematically, and which I think is also a nice fit for this kind of
application.  I've included a few examples of translating DSP difference
equations into Haskell code, that you could in turn use to generate known
correct output streams for a given input.

    -- input: impulse at time n=0
    -- at time zero, x has value 1.  at all other times, x has value 0.
    x 0 = 1.0
    x n = 0.0

    -- delay output by five samples
    y n = x (n-5)

    -- accumulate a list of xes and the corresponding ys
    xs = [ x(n) | n <- [0..40] ]
    ys = [ y(n) | n <- [0..40] ]

    -- print out the y values at each timestep
    main = print ys

As you can see, the equations for x and y are pretty simple.  There might be a
little learning of Haskell syntax to do to translate this to your own
application, but it should be worth it.

This approach has the same caveats as the first Python implementation, namely
that it doesn't cache values it might not work if you try to execute too deep a
recursion.

## The examples given

Here we list a directory of the examples that given in this project.

 - a comparison of delay implementations
 - a reverb (TODO)
 - waveguides and scattering junctions (TODO)

## Closing

This isn't really a very complicated idea.  It was mostly just to a) illustrate
a strategy that you can use when thinking through your implementation problems,
and b) for me to try out the "fancy" python implementation that caches values
and does some error checking.  Hopefully the examples here will give you some
ideas for ways to approach tricky implementations.

This document is licensed as Creative Commons CC BY-NC-SA.
The code in this project is hereby placed in the public domain.

Mark Zadel 2013

 vim:sw=4:ts=4:et:ai:
