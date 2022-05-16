# try to brute-force all the pie wedge orientation combinations
# (#,#,#,#) 0-3
# 0 is in, 2 is out, 1, and 3 are rotated left and right


def mirror(s):
    # convert 1 to 3, and 3 to 1
    # then reverse the direction
    l = [x for x in s]
    l.reverse()
    for i, e in enumerate(l):
        if e%2: l[i] = (e+2)%4
    return tuple(l)


def rotate(s):
    # shift the order one place
    l = [x for x in s]
    t = l.pop(0)
    l.append(t)
    return tuple(l)


# some test stuff
# t = (0,1,0,0)
# for i in range(8):
#     t = rotate(t)
#     print(t)

allstates = set()
for i in range(4):
    l = [i]
    for i in range(4):
        l.append(i)
        for i in range(4):
            l.append(i)
            for i in range(4):
                l.append(i)
                allstates.add(tuple(l))
                l.pop()
            l.pop()
        l.pop()

print(len(allstates))
uniquestates = set()
while len(allstates):
    s = allstates.pop()
    uniquestates.add(s)
    # remove all other permutations of s
    for i in range(3):
        s = rotate(s)
        if s in allstates:
            allstates.remove(s)
    sm = mirror(s)
    if sm != s:
        if sm in allstates:
            allstates.remove(sm)
        for i in range(3):
            sm = rotate(sm)
            if sm in allstates:
                allstates.remove(sm)
print(len(uniquestates))
l = list(uniquestates)
l.sort()
for i in l:
    print(i)
