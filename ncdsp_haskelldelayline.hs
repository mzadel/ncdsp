
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

printdelay n = print [ delay 0 n, delay 1 n, delay 2 n, delay 3 n, delay 4 n ]

main = do
	-- print delay line contents at time 0
	printdelay 0
	-- print delay line contents at time 1
	printdelay 1
	-- print delay line contents at time 2
	printdelay 2
	print xs
	print ys

