
-- input: impulse at time n=0
x 0 =  1.0
x n =  0.0
-- nb: x 0 has to be first here -- it matches them in order

-- delay output by five samples
y n = x $ n-5

-- a list of xes and the corresponding ys
xs = [ x n | n <- [0..40] ]
ys = [ y n | n <- [0..40] ]

main = print ys

-- this is actually quite clear...

