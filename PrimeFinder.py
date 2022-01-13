savefile = 'primes.txt'

from time import time as tm

try:
    # initialize with a list of primes
    # Interesting results if we leave some out?
    f = open(savefile, "r")
    prime_source = f.read()
    f.close()
    primes = sorted([ int(p) for p in prime_source.split() if p.isnumeric() ])
except:
    primes = [2, 3, 5, 7]
increment = primes[0]
candidate = primes[-1] + increment
# Generate primes in batches
# batch = 2027

while True:
    # save every couple minutes
    t = tm() + 120
    while tm() < t:
        #print(candidate)
        # halfcand = candidate / 2
        primecheck = True
        for factor in primes[1:]:
            #print(factor)
            if (candidate / factor) < factor: break
            if candidate % factor == 0:
                primecheck = False
                break
        if primecheck:
            print(candidate, "is prime")
            primes.append(candidate)
            # found += 1
        candidate += increment

    f = open(savefile, "w")
    for i in primes: f.write(str(i)+' ')
    f.close()
