# 3d print turbocharger
# changes all of the extrusion feed gcode speeds

fin = "1x_Portable_Cable_Winder_-_Large_CFS_3_Latch_Spring.gcode"
fout = 'testoutput.gcode'

newspeed = 'F6000'


f = open(fin,'r')
data = f.readlines()
f.close()
print(len(data))
print(data[:10])

newdata = []

for line in data:
    skip = False
    if line[0] == ';': skip = True
    if line[:2] == 'G0': skip = True
    if 'Z' in line: skip = True
    if 'F' not in line: skip = True
    if skip:
        newdata.append(line)
        continue
    secs = line.split(' ')
    for i, sec in enumerate(secs):
        if "F" != sec[0]: continue
        secs[i] = newspeed
    newline = ' '.join(secs)
    newdata.append(newline)
    

f = open(fout,'w')
for line in newdata:
    f.write(line)
f.close()
