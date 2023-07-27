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
    laserstr = "X{0} Y{0} M03 S{0} F{1}\n".format('{}', LASERFEED)
else:
    laserstr = "X{0} Y{0} M03 S{2} F{1}\n".format('{}', LASERFEED, LASERPOWER)
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
try: origin = (float(XYOr[0][1:]),float(XYOr[1][1:]))
except: origin = (0,0)
#print(origin)
# import all the points
points = []
splines = []
spline = []
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
        results.append(text[:nxtT])
        if nxtT < len(text): text = text[nxtT:]
        else: text = ""
    return results

def get_tokens(line):
    NCTokens = ("X", "Y", "F", "S", "M", "G")
    token_results = {}
    splits = multisplit(line, NCTokens)
    for seg in splits:
        try:
            token_results[seg[0]] = float(seg[1:].strip())
        except:
            pass
    return token_results

X = 0.
Y = 0.
S = 0

NC_lines = data[header_end:footer_pos].splitlines()

for NCLine in NC_lines:
    line_tokens = get_tokens(NCLine)
    if "X" in line_tokens: X = line_tokens["X"]
    if "Y" in line_tokens: Y = line_tokens["Y"]
    p = {"X": X, "Y": Y}
    if S != 0: p["S_reverse"] = S
    if "S" in line_tokens:
        S = int(line_tokens["S"])
        if S != 0: p["S_forward"] = S
    if (S == 0) and (len(spline) > 1):

        pass


while True:

    p = [X,Y,loop,S]
    if (S == 0) and (len(loop) == 1):
        loop = [p]
        p[2] = loop
    elif (S == 0) and (len(loop) > 1): pass
    else: loop.append(p)
    if ((S == 0 ) and (len(loop) > 1)):
        loops.append(loop)
        points.append(loop[0])
        loop = [p]
        p[2] = loop
    if nextX > footer_pos: break
    else: X_found = nextX

print('collected',len(points),'points in',len(loops),'loops')

# process them
#sort the loops by length?
##for loop in loops:
##    loop.append(len(loop))
##def k(l):
##    return l[-1]
##loops.sort(key=k, reverse=True)

def dist(p1,p2):
    return ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

curpos = origin
dataout = ""
while len(points):
    if len(points)%500 == 498:
        print('.',end='',flush=True)
    def close(p1): return dist(p1, curpos)
    points.sort(key=close)
    closest = points[0]
    #print(closest[:-1])
    loop = closest[2]
##    reordered = loop[:]
##    dataout += traversestr.format(closest[0],closest[1])
    #print(loop)
    points.remove(loop[0])
    for p in loop:
        #dataout += laserstr.format(p[0],p[1],randint(1,LASERPOWER))
        if p[3] > 0: dataout += laserstr.format(p[0],p[1],p[3])
        else: dataout += traversestr.format(p[0],p[1])
##        points.remove(p)
    #dataout += laserstr.format(pstrt[0],pstrt[1],randint(1,LASERPOWER))
    #dataout += laserstr.format(pstrt[0],pstrt[1],LASERPOWER)
    curpos = (loop[-1][0],loop[-1][1])

#save the file out
f = open(FILEOUT, 'w')
f.write(header)
f.write(dataout)
f.write(footer)
f.close()
