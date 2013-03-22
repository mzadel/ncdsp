
-- karplusstrong_memoized.hs

{-

Here's an example of memoizing one of the functions to make everything much,
much faster.  I had to experiment a bit -- it turned out to be faster if I only
memoized the filteroutput function and not the other ones.

It's a little less clear, but it's not too bad.

-}

import qualified Data.MemoCombinators as Memo

excitation 0 = 1.0
excitation n = 0.0

output n = (excitation n) + (filteroutput n)

delayinput n = output n
delaysamples = 50
delayoutput n = delayinput (n-delaysamples)

filterinput n = delayoutput n
-- need to specify a base case here since it's recursive with itself
filteroutput  = Memo.integral filteroutput'
    where
        filteroutput' n
          | n >= 0 = 0.5 * (filterinput n) + 0.5 * (filteroutput (n-1))
          | otherwise = 0.0

outsamples = [ output n | n <- [0..150] ]

main = do
  -- in the memoized version I can go up to much higher sample numbers
  -- memoizing filteroutput made a big difference
  -- without memoization this is basically impossible
  print (output 20000)

-- vim:sw=4:ts=4:et:ai
