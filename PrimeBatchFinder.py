BATCHFOLDER = 'batch_primes'
PREFIX = 'PrimesTo_'
SAVESTRIDE = 500000
SUFFIX = '.txt'
SAVEINTERVAL = 120  # seconds
BATCHMASK = 70  # no work on batches below this number

from time import time as tm
from os import stat

# Load moved inline
primes = []
cur_batch = -1
cur_limit = 0
increment = 2
while True:
    cur_batch += 1
    batch_new = True  # to reserve a save file on the first prime found
    cur_limit = (cur_batch + 1) * SAVESTRIDE
    savefile = f'{BATCHFOLDER}/{PREFIX}{cur_limit}{SUFFIX}'
    loaded = False
    newprimes = []
    try:
        f = open(savefile, "r")
        prime_source = f.read()
        f.close()
        gathered_primes = sorted([int(p) for p in prime_source.split() if p.isnumeric()])
        primes += gathered_primes
        del gathered_primes
        del prime_source
        loaded = True
    except:
        if len(primes) < 4:
            primes = [2, 3, 5, 7]
            loaded = True
            newprimes = primes[:]
        else: loaded = False
    if cur_batch < BATCHMASK: continue
    if loaded:
        # skip it if this file is being worked on recently
        try:
            if (stat(savefile).st_mtime + SAVEINTERVAL*1.618) > tm():
                print(f'Batch {cur_batch} appears to be already in work')
                continue
        except: pass
        candidate = primes[-1] + increment
    else:  # The current batch was not loaded, so
        candidate = cur_batch * SAVESTRIDE
        if candidate % 2 == 0: candidate += 1
    t: float = tm() + SAVEINTERVAL
    while candidate < cur_limit: # prime finder loop
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
        # before moving on to the next batch
        f = open(savefile, "a")
        for i in newprimes: f.write(str(i) + '\n')
        f.close()
        newprimes = []
    print(f'Primes in batch {cur_batch} completed')
