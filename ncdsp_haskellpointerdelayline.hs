
-- input: impulse at time n=0
x(0) = 1.0
x(1) = 2.0
x(2) = 3.0
x(n) = 0.0

-- pointer circulating around the array
pointer(n) = n `mod` 5

delaylinecontents cell n
	| cell == pointer(n) = x(n)
	| otherwise = delaylinecontents cell (n-1)

y(n) = delaylinecontents (pointer(n)) (n-1)

-- a list of xes and the corresponding ys
xs = [ x(n) | n <- [0..40] ]
ys = [ y(n) | n <- [0..40] ]

printdelay n = print [ delaylinecontents 0 n, delaylinecontents 1 n, delaylinecontents 2 n, delaylinecontents 3 n, delaylinecontents 4 n ]

main = do
	-- print delay line contents at time 0
	printdelay 0
	-- print delay line contents at time 1
	printdelay 1
	-- print delay line contents at time 2
	printdelay 2
	print xs
	print ys


