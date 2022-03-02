# Document parsing script
# For importing EXP files to Blender
# format info at https://www.appropedia.org/EXP_Embroidery_File_Format
# Another Python embroidery format converter at https://pypi.org/project/pyembroidery/

import bpy
import os
from mathutils import Vector

FILEIN = os.path.join(os.path.dirname(bpy.data.filepath), 'curls.exp')

#open the file and read it into memory as "data"
f = open(FILEIN, 'rb')
data = f.read()
f.close()

def bin_to_int(b):
    if type(b) is not int: b = int(b)
    if b == 128: return None
    elif b < 128: return b
    else: return -256 +b

curpos = [0,0]
points = []
lines = []
allsets = [(points,lines)]
Stitched = False
DoStitch = True
Skip = False

for i in range(len(data)//2):
    if Skip:
        Skip = False
        continue
    pair = data[i*2:i*2+2]
    if pair[0] == 128:
        if pair[1] == 1: # pause, follow by 0,0
            points = []
            lines = []
            allsets.append((points,lines))
            Stitched = False
            DoStitch = True
            Skip = True
            continue
        elif pair[1] == 2: # stitch (not used)
            pair = (0,0)
            DoStitch = True
        elif pair[1] == 4: # jump, follow by x,y
            DoStitch = False
            continue
        elif pair[1] == 128: # end, follow by 0,0
            break
        
    dx = bin_to_int(pair[0])
    dy = bin_to_int(pair[1])
    curpos[0] += dx
    curpos[1] += dy
    points.append((curpos[0],curpos[1]))
    if DoStitch:
        if Stitched:
            idx = len(points) - 1
            if idx > 0: lines.append((idx-1,idx))
        else:
            Stitched = True
    else: DoStitch = True

context = bpy.context
layer = context.view_layer
layer_collection = context.layer_collection or layer.active_layer_collection
scene_collection = layer_collection.collection

for color in allsets:
    verts = [Vector((vrt[0], vrt[1], 0)) for vrt in color[0]]
    edges = color[1]
    name = "Embroidery"
    mesh = bpy.data.meshes.new(name=name)
    faces = []
    mesh.from_pydata(verts, edges, faces)
    obj_new = bpy.data.objects.new(name, mesh)
    scene_collection.objects.link(obj_new)
