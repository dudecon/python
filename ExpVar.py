import math, random

# a random number generator designed to average out to 1
# range boundaries are 1/variance to variance
# the corrected version boosts the numbers to correct the average
# for finite sample sizes (tuned to about 2 million).

def expvar(variance):
    alpha = 0.5*math.log(variance)+2
    rndfac = 1 - 2 * random.betavariate(alpha,2)
    curval = variance**rndfac
    return curval

def expvar_corr(variance):
    if variance <= 1: return 1
    corrTable = [1.0, 1.1, 1.3, 1.6, 2.0, 2.6, 3.2, 4.2, 6.7, 8.1, 14., 46.]
    corrMaxIdx = len(corrTable) - 1
    interp = math.log(variance, 10)
    if interp >= corrMaxIdx:
        variance = 10**corrMaxIdx
        correction = corrTable[corrMaxIdx]
    else:
        #do a linear interpolation
        i = math.floor( interp )
        lower = corrTable[i]
        upper = corrTable[i+1]
        diff = upper-lower
        offset = interp - lower
        correction = lower + offset*diff
    curval = correction * expvar(variance)
    return curval
