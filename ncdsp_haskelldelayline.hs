
-- input: impulse at time n=0
x(0) = 1.0
x(1) = 2.0
x(2) = 3.0
x(n) = 0.0

-- delay line takes its first cell's input from the current value of x(n)
delay 0 n = x(n)
delay cell n = delay (cell-1) (n-1)

-- y(n) takes its value from the outgoing contents of the fifth cell of the
-- delay line (which is at index 4)
y(n) = delay 4 (n-1)

-- a list of xes and the corresponding ys
xs = [ x(n) | n <- [0..40] ]
ys = [ y(n) | n <- [0..40] ]

main = do
	print xs
	print ys

