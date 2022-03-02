# Document parsing script
# Trying to tease apart EXP files
# format info at https://www.appropedia.org/EXP_Embroidery_File_Format
# Another Python embroidery format converter at https://pypi.org/project/pyembroidery/

import bpy
import os
from mathutils import Vector

FILEOUT = os.path.join(os.path.dirname(bpy.data.filepath), 'curls.exp')

def bin_to_int(b):
    if type(b) is not int: b = int(b)
    if b == 128: return None
    elif b < 128: return b
    else: return -256 +b

def int_to_bin(i):
    if type(i) is not int: i = int(i)
    if i < -127: return None
    elif i > 127: return None
    elif i < 0: b = i + 256
    else: b = i
    return b.to_bytes(1,'big')

lastpos = [0.,0.]

def mv(d):
    dx = d[0]
    dy = d[1]
    if (dx == 0) and (dy == 0): return b'\x00\x00'
    b = b''
    while dx or dy:
        if (abs(dx) > 127) or (abs(dy) > 127):
            b += b'\x80\x04'
        positive = [(abs(d) == d) for d in (dx, dy)]
        xstp = min(abs(dx),127)
        if not positive[0]: xstp *= -1
        ystp = min(abs(dy),127)
        if not positive[1]: ystp *= -1
        b += int_to_bin(xstp)
        b += int_to_bin(ystp)
        dx -= xstp
        dy -= ystp
    return b

context = bpy.context
objects = context.selected_objects

ctvrs = {}
ctvrs['data'] = b''
ctvrs['points'] = []
ctvrs['lines'] = []
ctvrs['ptidx'] = 0
ctvrs['lastpos'] = [0.,0.]

def traverse(ctvrs):
    pos = ctvrs['points'][ctvrs['ptidx']]
    d = [round(pos[i] - ctvrs['lastpos'][i]) for i in (0,1)]
    for i in (0,1):
        ctvrs['lastpos'][i] += d[i]
    ctvrs['data'] += mv(d)
    found = False
    for ln in ctvrs['lines']:
        if ln[0] == ctvrs['ptidx']:
            ctvrs['ptidx'] = ln[1]
            found = True
        elif ln[1] == ctvrs['ptidx']:
            ctvrs['ptidx'] = ln[0]
            found = True
        if found:
            ctvrs['lines'].remove(ln)
            break

for ob in objects:
    ctvrs['points'] = [(vt.co[0], vt.co[1]) for vt in ob.data.vertices]
    ctvrs['lines'] = ob.data.edge_keys
    ctvrs['ptidx'] = 0
    traverse(ctvrs)
    while len(ctvrs['lines']):
        traverse(ctvrs)
    traverse(ctvrs)
    ctvrs['data'] += b'\x80\x01\x00\x00'

# end of file tag
data = ctvrs['data']
data = data[:-4] # strip the last pause command
data += b'\xff\xff\x00\x00'

f = open(FILEOUT, 'wb')
f.write(data)
f.close()

