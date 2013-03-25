
-- karplusstrong_audio.hs

{-

An implementation of the karplus-strong algorithm that generates audio.
The sound output is written out to /tmp/output.wav.
We need to cache the values computed by filteroutput so it runs in a reasonable
timeframe.

-}

import qualified Data.MemoCombinators as Memo
import Data.WAVE

excitation 0 = 1.0
excitation 1 = -1.0
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




samplerate = 44100
numberofsamples = samplerate * 5
-- compute a list of values [ v1, v2, v3, ... ] for each timestep
values = map output [0..(numberofsamples-1)]
-- format the sample list to pass to putWAVEFile
samplestowriteout = [ [doubleToSample x] | x <- values ]




main = do
    putWAVEFile "/tmp/output.wav" (WAVE (WAVEHeader 1 samplerate 32 Nothing) samplestowriteout)


-- vim:sw=4:ts=4:et:ai
