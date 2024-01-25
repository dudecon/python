# Try to brute-force all the pie wedge orientation combinations
# (#,#,#,#) 0-3
# 0 is in, 2 is out, 1, and 3 are rotated left and right

def mirror(s):
    # Convert 1 to 3, and 3 to 1
    # Then reverse the direction
    return tuple((x + 2) % 4 if x % 2 else x for x in reversed(s))

def rotate(s):
    # Shift the elements one place to the left
    return s[1:] + (s[0],)

allstates = [(i, j, k, l) for i in range(4) for j in range(4) for k in range(4) for l in range(4)]

uniquestates = []
print(len(allstates), " total states")
while allstates:
    s = allstates.pop()
    uniquestates.append(s)
    # Remove all other permutations of s
    allstates = [
        x for x in allstates if x not in (
            s, rotate(s), rotate(rotate(s)), rotate(rotate(rotate(s))),
            mirror(s), mirror(rotate(s)), mirror(rotate(rotate(s))), mirror(rotate(rotate(rotate(s))))
        )
    ]

uniquestates.sort()
for i in uniquestates:
    print(i)

print(len(uniquestates), " unique states")
