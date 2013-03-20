
--karplusstrong.hs

{-
The Karplus-Strong string synthesis algorithm.

The only problem here is that it's extremely slow (since there's no memoization
here), so you wouldn't be able to use this to generate actual audio data.
-}


excitation 0 = 1.0
excitation n = 0.0

output n = (excitation n) + (filteroutput n)

delayinput n = output n
delaysamples = 50
delayoutput n = delayinput (n-delaysamples)

filterinput n = delayoutput n
-- need to specify a base case here since it's recursive with itself
filteroutput n
  | n >= 0 = 0.5 * (filterinput n) + 0.5 * (filteroutput (n-1))
  | otherwise = 0.0

outsamples = [ output n | n <- [0..150] ]

main = do
  --print outsamples
  print (output 200)   -- just compute one; goes relatively quickly

