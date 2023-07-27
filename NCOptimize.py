# Document parsing script
# Replace newline characters with space
# except when immediately following a > symbol

FILEIN = 'MooseAlone.nc'
FILEOUT = FILEIN.replace('.',' Optimum.',1)

LASERFEED = 700
RAPIDFEED = 1200
LASERPOWER = 256

# from random import randint
from math import sqrt

traversestr = "X{0} Y{0} M03 S0 F{1}\n".format('{}',RAPIDFEED)
#print(traversestr)
laserstr = "X{0} Y{0} M03 S{0} F{1}\n".format('{}',LASERFEED)
#laserstr = "X{0} Y{0} M03 S{2} F{1}\n".format('{}',LASERFEED,LASERPOWER)
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

header = data[:pos_found+len(header_end_strs[i])]
print("header:\n",header)
# find the origin
XYOr = header.split()[-3:-1]
try: origin = (float(XYOr[0][1:]),float(XYOr[1][1:]))
except: origin = (0,0)
#print(origin)
# import all the points
points = []
loops = []
loop = []
search_from = pos_found +1
footer_end_strs = ("M05 ","M5 ")
footer_pos = -1
i = -1
while footer_pos == -1:
    i += 1
    footer_pos = data.find(footer_end_strs[i],search_from)

Y_end = 0
X = 0.
Y = 0.
S = 0
X_found = data.find("X",search_from)
while True:
    #X_found = data.find("X",Y_end)
    Y_found = data.find("Y",X_found)
    X_end = min(data.find(" ",X_found),data.find("\n",X_found),data.find("F",X_found) , Y_found)
    X = float(data[X_found+1:X_end])
    nextX = data.find("X",X_found+1)
    if nextX == -1: break
    if Y_found < nextX:
        Y_end = min(data.find(" ",Y_found),data.find("\n",Y_found),data.find("F",Y_found))
        if Y_end == -1: break
        Y = float(data[Y_found+1:Y_end])
    s_found = data.find("S",X_found)
    if s_found < nextX:
        s_end = data.find("\n",s_found)
        if s_end == -1: break
        S = int(data[s_found+1:s_end])
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

footer = data[footer_pos:]
print("footer:\n",footer)

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
