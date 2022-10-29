# Dorfromantik spot finder and logger thing

# tile match locations are noted in CW order with a single character
# --------------------------------
# Tile edge condition key
# a : any (use only as a spacer for empty edges)
# f : field (matches with water)
# t : trees and forest
# c : city and houses
# v : river (matches water)
# r : railroad
# w : water (matches field and river)
# s : water station (matches field, river, rail, and water)

EdgeChrs = "AFTRVWCS"
EdgeKey = "Field, Tree, City, riVer, Railroad, Water, Station"
instructions = f"""record spots with several constrained edges
{EdgeKey}
to search against the existing locations
enter the six character edge key string (clockwise order).
If less than six are entered, the final character will be repeated to pad it out
To record a new location, prefix it with N followed by the string
if you want to make a note on the location of the tile, add it after a space
To delete a location that you have matched, prefix with D and then the
number of the location.
To modify a location, prefix with M and then the index number, and then the
new edge key.
Type X or Q to save and quit
To list jus the edge keys, type ?
Type anything else to bring up this help text again
"""

SaveFile = "Dorfromantik_Helper.txt"

def isvalidedges(edgstr):
    for c in edgstr:
        if c not in EdgeChrs: return False
    return True

try:
    f = open(SaveFile, 'r')
    allspots = eval(f.read())
    f.close()
except:
    allspots = {}

def compatedge(c1, c2):
    if c1 == c2: return True # like matches like
    if (c1 == "A") | (c2 == "A"): return True
    if (c1 == "W") & (c2 in "FV"): return True
    if (c2 == "W") & (c1 in "FV"): return True
    if (c1 == "S") & (c2 in "WFVR"): return True
    if (c2 == "S") & (c1 in "WFVR"): return True
    return False

def edgesmatch(st1, st2):
    # the first arg should be the shorter string
    st2len = len(st2)
    for sti in range(st2len):
        i = sti
        for c in st1:
            if compatedge(st2[i], c):
                i += 1
                i %= st2len
            else: break
        else:
            #for loop exhausted, so we have a match
            return True
    return False

print(instructions)
# main control loop

foundspots = [i for i in allspots]

while True:
    foundspots.sort(reverse=True, key=lambda x: len(x))
    foundspots = foundspots[:10]
    for i, k in enumerate(foundspots):
        print(i, k, allspots[k])
    RawIn = input("now choose: ").strip()
    if len(RawIn) == 0:
        print(instructions)
        continue
    SplIn = RawIn.split()
    FirstIn = SplIn[0].upper()
    if len(SplIn) > 1: LastIn = ' '.join(SplIn[1:])
    else: LastIn = ""
    if FirstIn == "?": print(EdgeKey)
    elif FirstIn[0] == "D":
        if len(FirstIn) == 1: FirstIn += "0"
        try:
            idx = int(FirstIn[1])
            sqnc = foundspots[idx]
            del(allspots[sqnc])
            del(foundspots[idx])
            print(f"{sqnc} deleted")
        except:
            print("That didn't work for some reason")
    elif FirstIn[0] == "N":
        if len(FirstIn) > 7:
            print("unusually long location string. Please use caution!")
        key = FirstIn[1:]
        if isvalidedges(key):
            allspots[key] = LastIn
            foundspots = []
            print(f"new location {key} recorded")
        else:
            print("Not a valid location")
    elif FirstIn[0] == "M":
        try:
            idx = int(FirstIn[1])
            sqnc = foundspots[idx]
            key = FirstIn[2:]
            if not isvalidedges(key):
                print("Not a valid location")
                continue
            del(allspots[sqnc])
            allspots[key] = LastIn
            foundspots = []
            print(f"{sqnc} changed to {key}")
        except:
            print("That didn't work for some reason")
    elif isvalidedges(FirstIn):
        # search for any matching spots
        lfi = len(FirstIn)
        if lfi > 6: FirstIn = FirstIn[:6]
        elif lfi<6: FirstIn += FirstIn[-1]*(6-lfi)
        foundspots = [i for i in allspots if edgesmatch(i, FirstIn)]
    elif (FirstIn[0] == "X") | (FirstIn[0] == "Q"):
        print("save and close")
        f = open(SaveFile, 'w')
        f.write(str(allspots))
        f.close()
        break
    else: print(instructions)
