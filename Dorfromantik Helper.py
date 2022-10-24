# Dorfromantik spot finder and logger thing

# tile match locations are noted in CW order with a single character
# --------------------------------
# Tile edge condition key
# a : any (use only as a spacer for empty edges)
# f : field (matches with water)
# t : trees and forest
# c : city and houses
# r : river (matches water)
# l : railroad
# w : water (matches field and river)
# s : water station (matches field, river, rail, and water)

EdgeChrs = "AFTRCLWS"
EdgeKey = "Field, Tree, City, River, raiLroad, Water, Station"
instructions = f"""record spots with 3 or more constrained edges
{EdgeKey}
if you are entering a new tile to check it against the existing locations
simply enter the six character edge key string (clockwise order)
To record a new location, prefix it with N followed by the string
if you want to make a note on the location of the tile, add it after a space
To delete a location that you have matched, prefix with D. Multiple matches
will bring up a menu to select the spot you want.
Type X or Q to save and quit
"""

SaveFile = "Dorfromantik_Helper.txt"

def isvalidedges(edgstr):
    for c in edgstr:
        if c not in EdgeChrs: return False
    return True

allspots = {}

def compatedge(c1, c2):
    if c1 == c2: return True # like matches like
    if c1 == "A" | c2 == "A": return True
    if c1 == "W" & c2 in "FR": return True
    if c2 == "W" & c1 in "FR": return True
    if c1 == "S" & c2 in "WFRL": return True
    if c2 == "S" & c1 in "WFRL": return True
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
while True:
    RawIn = input().strip()
    SplIn = RawIn.split()
    FirstIn = SplIn[0].upper()
    if len(SplIn) > 1: LastIn = ' '.join(SplIn[1:])
    else: LastIn = ""
    # print(FirstIn, "and", LastIn)
    # continue
    if FirstIn[0] == "D":
        print("placeholder for delete")
    elif FirstIn[0] == "N":
        key = FirstIn[1:]
        if isvalidedges(key):
            allspots[key] = LastIn
            print(f"new location {key} recorded")
        else:
            print("Not a valid location")
        
    elif isvalidedges(FirstIn):
        if 'A' in FirstIn:
            print("the Any wildcard isn't meant for checks.\nPlease enter all six actual edge keys")
            continue
        if len(FirstIn) != 6:
            print("please enter all six edges")
            continue
        print("placeholder for check tile")
        for spot in allspots:
            if edgesmatch(spot, FirstIn):
                print(spot, end=" ")
                val = allspots[spot]
                if len(val): print(val)
    elif (FirstIn[0] == "X") | (FirstIn[0] == "Q"):
        print("save and close")
        break
    else: print(instructions)
