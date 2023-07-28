# NC code optimization code
# Released to the Public Domain by Paul Spooner
# Designed for driving my laser engraver

FILEIN = 'MooseAlone.nc'
FILEOUT = FILEIN.replace('.',' Optimum.',1)

LASERFEED = 700
RAPIDFEED = 1200
LASERPOWER = 256
VARIABLEPOWER = False

# from random import randint
from math import sqrt

traversestr = "X{0} Y{0} M03 S0 F{1}\n".format('{}',RAPIDFEED)
#print(traversestr)
if VARIABLEPOWER:
    laserstr = "X{0} Y{0} S{0} F{1}\n".format('{}', LASERFEED)
else:
    laserstr = "X{0} Y{0} F{1}\n".format('{}', LASERFEED)
#print(laserstr)

#open the file and read it into memory as "data"
f = open(FILEIN, 'r')
data = f.read()
f.close()

header_end_strs = ("M03 S0\n","M3 S0\n")
pos_found = -1
i = -1
while pos_found == -1:
    i += 1
    pos_found = data.find(header_end_strs[i],0)

header_end = pos_found+len(header_end_strs[i])
header = data[:header_end]

# print("header:\n",header)
# find the origin
XYOr = header.split()[-3:-1]
try: origin = {"X": float(XYOr[0][1:]), "Y": float(XYOr[1][1:])}
except: origin = {"X": 0, "Y": 0}
#print(origin)
# import all the points
search_from = pos_found +1
footer_end_strs = ("M05 ","M5 ")
footer_pos = -1
i = -1
while footer_pos == -1:
    i += 1
    footer_pos = data.find(footer_end_strs[i],search_from)

footer = data[footer_pos:]
#print("footer:\n",footer)

def multisplit(text, tokens):
    results = []
    while len(text):
        nxtT = len(text)
        for t in tokens:
            found = text.find(t, 1)
            if found >= 0: nxtT = min(nxtT, found)
        results.append(text[:nxtT].strip())
        if nxtT < len(text): text = text[nxtT:]
        else: text = ""
    return results

def get_tokens(line):
    NCTokens = ("X", "Y", "F", "S", "M", "G")
    token_results = {}
    splits = multisplit(line.strip(), NCTokens)
    for seg in splits:
        if seg[0] in NCTokens:
            try:
                token_results[seg[0]] = float(seg[1:].strip())
            except:
                pass
    return token_results

def areSamePosition(p1, p2):
    if p1["X"] != p2["X"]: return False
    if p1["Y"] != p2["Y"]: return False
    return True

numPoints = 0
splines = []
loops   = []
spline  = []
X = 0.
Y = 0.
S =  0

NC_lines = data[header_end:footer_pos].splitlines()

for NCLine in NC_lines:
    line_tokens = get_tokens(NCLine)
    if "X" in line_tokens: X = line_tokens["X"]
    if "Y" in line_tokens: Y = line_tokens["Y"]
    if "S" in line_tokens: S = line_tokens["S"]
    if ("X" in line_tokens) or ("Y" in line_tokens):
        p = {"X": X, "Y": Y}
    else:
        # no new position info, so continue processing
        continue
    if (S != 0) and VARIABLEPOWER: p["S_reverse"] = S
    if "S" in line_tokens:
        S = int(line_tokens["S"])
        if (S != 0) and VARIABLEPOWER: p["S_forward"] = S
    if S == 0:
        if len(spline) > 1:
            # we need at least two points for a valid spline
            if areSamePosition(spline[0], spline[-1]):
                spline.pop(-1)
                if VARIABLEPOWER:
                    # loop the power values
                    spline[0]["S_reverse"]  = spline[-1]["S_reverse"]
                    spline[-1]["S_forward"] =  spline[0]["S_forward"]
                loops.append(spline)
            else:
                splines.append(spline)
            numPoints += 1
        else:
            # no new point data, so don't increment point data
            pass
        # either way, start a new spline
        spline = [p]
    else:
        # just add the point data to the existing spline
        spline.append(p)
        numPoints += 1

print('collected',numPoints,'points in',len(loops),'loops and',len(splines),'splines.')

# process them

def dist(p1,p2):
    return (p1["X"] - p2["X"])**2 + (p1["Y"] - p2["Y"])**2

pointstosearch = []
for spline in splines:
    for i in (0, -1):
        endpoint = spline[i]
        endpoint["type"]   = i
        endpoint["group"]  = spline
        pointstosearch.append(endpoint)
for loop in loops:
    loopLen = len(loop)
    loopPointDivisor = max(1, 5//loopLen)
    for i in range(loopLen // loopPointDivisor):
        idx = i*loopPointDivisor
        looppoint = loop[idx]
        looppoint["type"]  = 1
        looppoint["group"] = loop
        looppoint["idx"]   = idx
        pointstosearch.append(looppoint)

TypeToKey = {-1:"S_reverse", 0:"S_forward", 1:"S_forward"}

curpos = origin
OutString = header

def close(p1): return dist(p1, curpos)

while len(pointstosearch):
    pointstosearch.sort(key=close)
    # if VERBOSE: print(pointstosearch)
    curpos = pointstosearch[0]
    grp = curpos['group']
    # purge the search list
    to_remove = []
    for pnt in pointstosearch:
        if pnt['group'] is grp:
            del pnt['group']
            to_remove.append(pnt)
    for pnt in to_remove:
        pointstosearch.remove(pnt)
    # re-order the group found
    posType = curpos["type"]
    if posType == 1:
        # it's a loop
        pidx = curpos['idx']
        grp = grp[pidx:] + grp[:pidx]
        grp.append(grp[0])
    else:
        # it's an open curve
        if posType == -1:
            grp.reverse()
    X = curpos['X']
    Y = curpos['Y']
    # for each segment or loop, jog to the start, turn on the laser, complete the path, and turn off again.
    OutString += f"G00 X{X:.2f} Y{Y:.2f} F{RAPIDFEED}\n"
    # M03 is spindle on, s is the spindle speed (or laser power in this case), from 0 to 255
    if VARIABLEPOWER:
        # Laser power is not uniform, so don't assign here
        OutString += f"G1\n"
    else:
        OutString += f"G1 S{LASERPOWER}\n"

    if VARIABLEPOWER:
        for curpoint in grp[1:]:
            curpos = curpoint
            X = curpos['X']
            Y = curpos['Y']
            powerkey = TypeToKey[curpos["type"]]
            OutString += laserstr.format(X,Y,curpos[powerkey])
    else:
        for curpoint in grp[1:]:
            curpos = curpoint
            X = curpos['X']
            Y = curpos['Y']
            # G01 is linear motion
            OutString += laserstr.format(X,Y)
    # when done, turn the laser back off
    OutString += "M03 S0\n"

# when all the engraving is done, turn the laser off and jog back to the origin
OutString += "M05\n"
OutString += f"G00 X0 Y0 F{RAPIDFEED}\n"

#save the file out
f = open(FILEOUT, 'w')
f.write(OutString)
f.close()
