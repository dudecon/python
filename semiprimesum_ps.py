
primes = []
f = open("primes.txt", "r")
'''l = f.readline().split()
l = f.readline().split()
while True:
    l = f.readline()
    if l is None: break
    primes += [int(x.strip()) for x in l.split()]'''
prime_source = f.read()
f.close()
primes = sorted([ int(p) for p in prime_source.split() if p.isnumeric() ])

# semiprime sum is a product of prime A and prime B
# start at the first prime, and add and multiply to check

# the index of each number is iA and iB
# increment through all primes from start to finish, and log all
# the ones that are a correct product

#upper_limit = 50000
upper_limit = len(primes)
start = 0
prev_iB = start
running_sum = primes[start]
for iA in range(start, upper_limit):
    # start at A and keep moving up the list checking
    # all the values of B
    A = primes[iA]
    #print(iA, prev_iB)
    for iB in range(prev_iB + 1, upper_limit):
        B = primes[iB]
        #print(iB)
        # every time you move to the next B, add it to the running sum
        running_sum += B
        semiprime = A * B
        difference = running_sum - semiprime
        # Through testing, I have found that there is a "pivot"
        # where lower values of B result in difference being negative
        # and higher values result in B being progressively more positive
        # I'm sure there's a faster way to search for this pivot, but I'm
        # just moving from the bottom up and quitting if it goes positive
        
        #print(A, B, semiprime, difference)
        if difference >= 0:
            #ratio = B / A
            if difference == 0: print(A, B, semiprime)
            #print((running_sum * B)/((running_sum - difference) * A))
            prev_iB = iB
            running_sum -= A
            break
    # if the difference is still negative by the time we reach the largest
    # prime, then our list of primes isn't large enough, quit while you're ahead
    if difference < 0: break
    
