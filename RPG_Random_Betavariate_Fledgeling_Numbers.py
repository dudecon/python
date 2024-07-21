from random import betavariate
from math import log, sqrt

Φ = 1.6180339887499

def randExpVariate(skew = 1):
    if skew < 1: raise OutOfRange
    α = Φ**2
    sk = Φ**α + skew**(2-Φ)
    growthfactor = log(skew, sk) + Φ**-(2-Φ)
    β = (2-Φ) + Φ**growthfactor
    exponent = betavariate(α,β)*2 - 1
    value = skew**exponent
    return(value)

def numtest(skew = 1,samples = 100):
    runningave = 0
    maxnum = 0
    for i in range(samples):
        value = randExpVariate(skew)
        #print(value)
        maxnum = max(maxnum,value)
        if i == 0: runningave = value
        else: runningave = (runningave*(i) + value ) / (i+1)
    print(f"average is {runningave:<6.5} with a skew of {skew:<6}, max was {maxnum:<6.5}")

if __name__ == '__main__':
    samples = 65437
    print(f'running {samples} samples. Average should be close to 1')
    testskews = (1,1.1,1.7,2,5,19,31,71,127,401,751,1217,2659)
    for i in testskews:
        numtest(i,samples)
    highvariance = 2659
    print(f'here are examples of skew = {highvariance}')
    while True:
        input("Press enter for another set:")
        for i in range(12):
            v = randExpVariate(highvariance)
            print(f'{v:0.5}')
        


