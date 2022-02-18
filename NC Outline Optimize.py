# Document parsing script
# Replace newline characters with space
# except when immediately following a > symbol

FILEIN = 'pawn.nc'
FILEOUT = FILEIN.replace('.',' Optimum.',1)

LASERFEED = 1200
RAPIDFEED = 2000
LASERPOWER = 255

from random import randint
from math import sqrt

traversestr = "G01 X{0} Y{0} M03 S0 F{1}\n".format('{}',RAPIDFEED)
#print(traversestr)
#laserstr = "X{0} Y{0} M03 S{0} F{1}\n".format('{}',LASERFEED)
laserstr = "X{0} Y{0} M03 S{2} F{1}\n".format('{}',LASERFEED,LASERPOWER)
#print(laserstr)

#open the file and read it into memory as "data"
f = open(FILEIN, 'r')
data = f.read()
f.close()

pos_found = data.find("G01 ",0)
header = data[:pos_found]
# find the origin
XYOr = header.split()[-3:-1]
origin = (float(XYOr[0][1:]),float(XYOr[1][1:]))
#print(origin)
# import all the points
points = []
loops = []
loop = []
search_from = pos_found +1
Y_end = 0
X_found = data.find("X",pos_found)
nextG1 = data.find("G01 ",X_found)
lastloop = False
while True:
    Y_found = data.find("Y",X_found)
    if Y_found == -1: break
    X = float(data[X_found+1:Y_found-1])
    Y_end = data.find(" ",Y_found)
    if Y_end == -1: break
    Y = float(data[Y_found+1:Y_end])
    X_found = data.find("X",Y_end)
    if X_found == -1: break
##    p = (X,Y,loop)
##    loop.append(p)
##    points.append(p)
    if X_found > nextG1:
        if lastloop: break
        nextG1 = data.find("G01 ",X_found)
        if nextG1 == -1:
            lastloop = True
            nextG1 = data.find("M03 S0\nM05",Y_end)
        loops.append(loop)
        loop = []
    else:
        p = (X,Y,loop)
        loop.append(p)
        points.append(p)
        
loops.append(loop)
pos_found = data.find("M03 S0\nM05",Y_end)
footer = data[pos_found:]

print('collected',len(points),'points in',len(loops),'loops')

# process them
#sort the loops by length?
##for loop in loops:
##    loop.append(len(loop))
##def k(l):
##    return l[-1]
##loops.sort(key=k, reverse=True)

def dist(p1,p2):
    return sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

curpos = origin
dataout = ""
while len(points):
    def close(p1): return dist(p1, curpos)
    points.sort(key=close)
    closest = points[0]
    #print(closest[:-1])
    loop = closest[2]
    loops.remove(loop)
    idx = loop.index(closest)
    reordered = loop[idx+1:] + loop[:idx+1]
    dataout += traversestr.format(closest[0],closest[1])
    #print(loop)
    for p in reordered:
        #dataout += laserstr.format(p[0],p[1],randint(1,LASERPOWER))
        dataout += laserstr.format(p[0],p[1])
        points.remove(p)
    #dataout += laserstr.format(pstrt[0],pstrt[1],randint(1,LASERPOWER))
    #dataout += laserstr.format(pstrt[0],pstrt[1],LASERPOWER)
    curpos = (closest[0],closest[1])

#save the file out
f = open(FILEOUT, 'w')
f.write(header)
f.write(dataout)
f.write(footer)
f.close()
