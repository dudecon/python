BATCHFOLDER = 'batch_primes'
PREFIX = 'PrimesTo_'
SAVESTRIDE = 500000
SUFFIX = '.txt'
SAVEINTERVAL = 120  # seconds

from time import time as tm
import os

# Load
primes = []
lastprimeperbatch = []
lastmodifiedbatch = []
cur_batch = 0
while True:
    try:
        cur_batch += SAVESTRIDE
        loadfile = f'{BATCHFOLDER}/{PREFIX}{cur_batch}{SUFFIX}'
        f = open(loadfile, "r")
        prime_source = f.read()
        f.close()
        gathered_primes = sorted([int(p) for p in prime_source.split() if p.isnumeric()])
        primes += gathered_primes
        lastprimeperbatch.append(gathered_primes[-1])
        del gathered_primes
    except:
        break
if len(primes) < 4: primes = [2, 3, 5, 7]

cur_batch = -1
cur_limit = 0
increment = primes[0]
while True:
    cur_batch += 1
    batch_new = True  # to reserve a save file on the first prime found
    cur_limit = (cur_batch + 1) * SAVESTRIDE
    savefile = f'{BATCHFOLDER}/{PREFIX}{cur_limit}{SUFFIX}'
    if cur_batch < len(lastprimeperbatch):
        # skip it if this file is being worked on
        if (os.stat(savefile).st_mtime + SAVEINTERVAL*1.618) > tm(): continue
        # otherwise, start at the cached last prime in the file
        candidate = lastprimeperbatch[cur_batch] + increment
    else:
        candidate = cur_batch * SAVESTRIDE
        if candidate % 2 == 0: candidate += 1
    t: float = tm() + SAVEINTERVAL
    newprimes = []
    while candidate < cur_limit:
        primecheck = True
        for factor in primes[1:]:
            if (candidate / factor) < factor: break
            if candidate % factor == 0:
                primecheck = False
                break
        if primecheck:
            print(candidate, "is prime")
            primes.append(candidate)
            newprimes.append(candidate)
            # check if we need to save the file
            if batch_new or (tm() > t):
                batch_new = False
                t = tm() + SAVEINTERVAL
                f = open(savefile, "a")
                for i in newprimes: f.write(str(i) + '\n')
                f.close()
                newprimes = []
        candidate += increment
    if len(newprimes):
        # save out the last of the new primes
        f = open(savefile, "a")
        for i in newprimes: f.write(str(i) + '\n')
        f.close()
        newprimes = []
    print(f'Primes in batch {cur_batch} completed')

# find the next batch of primes to work on
# increment the batch number, starting at zero
# check if there are remaining primes in this batch
# this will waste a little time at startup, but it should be okay.
# if there are, check the file modified time (cache this at load?)
# if the file has been saved recently, skip to the next batch
# if the file has not been saved, save out the new prime, and then work on this batch
# if this is a new batch, save the file with the first found prime
# to reserve this batch
