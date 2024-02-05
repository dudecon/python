#3d data convertor from .mu to .obj

# read in the file
# modify the contents
# write out to the new file


#file to read in
#should probably be a ".ma" file
filein = 'juggernaut_model.ma'

#file to read out
#should probably be a ".obj" file
fileout = 'juggernaut_model.obj'

#----------
# bones below. edit at your own risk
#----------

f = open(filein, 'r')
rawdata = f.read()
f.close()
#maybe these are a problem?
#for character in '/':
#    rawdata = rawdata.replace(character, '')


#Mesh format is a dictionary
#"Name": string with the mesh name
#"Verts": list of vertexes as three float tuples (x, y, z)
#"Faces": list of faces, tuple of absolute vertex indexes
#"DataPosition": position in the original file data where the mesh begins

def findString(data, start):
    #return the start and end points of the first " delimited string
    found_string_start = data.find('"', start) + 1
    found_string_end = data.find('"', found_string_start)
    return (found_string_start, found_string_end)

def findVerts(data, start):
    #return the start and end point of a vertex data block
    vertex_start_tag = '\n	setAttr ".vt['
    vertex_end_start_tag = ']"'
    vertex_end_tag = ";"
    found_vert_tag_pos = rawdata.find(vertex_start_tag, start)
    if found_vert_tag_pos == -1: return (-1,-1)
    found_vert_start_pos = rawdata.find(vertex_end_start_tag,
                            found_vert_tag_pos) + len(vertex_end_start_tag)
    if found_vert_start_pos == -1: return (-1,-1)
    found_vert_end_pos = rawdata.find(vertex_end_tag, found_vert_start_pos)
    if found_vert_end_pos == -1: return (-1,-1)
    return (found_vert_start_pos, found_vert_end_pos)
    
    

#find all the mesh objects
curpos = 0
mesh_list = []
mesh_tag = '\ncreateNode mesh '

#tag all the meshes
while True:
    found_mesh = rawdata.find(mesh_tag, curpos)
    if found_mesh == -1: break
    mesh_list += [{"DataPosition":found_mesh}]
    curpos = found_mesh + len(mesh_tag)
#get the mesh names
for msh_idx, mesh_data in enumerate(mesh_list):
    #get the name of the mesh
    string_1  = findString(rawdata, mesh_data["DataPosition"])
    Name_Location = findString(rawdata, string_1[1]+1)
    #print(Name_Location)
    if Name_Location[0] <= -1: break
    if Name_Location[1] <= -1: break
    MeshName = rawdata[Name_Location[0]:Name_Location[1]]
    mesh_data["Name"] = MeshName
    print(mesh_data)
    #get the vertex data
    # need the next mesh vert data, so we don't overlap
    if msh_idx == len(mesh_list) - 1: next_mesh_pos = len(rawdata)
    else: next_mesh_pos = mesh_list[msh_idx + 1]["DataPosition"]
    curpos = Name_Location[1]
    while True:
        #print(curpos)
        found_vert_data = findVerts(rawdata, curpos)
        #print(found_vert_data)
        if found_vert_data[0] <= -1: break
        if found_vert_data[1] <= -1: break
        if found_vert_data[1] >= next_mesh_pos: break
        # the raw vertex string
        vert_data_raw = rawdata[found_vert_data[0]:found_vert_data[1]]
        #print(vert_data_raw[:30],"-lots-of-verts-", vert_data_raw[-30:])
        #the simple values split into a list
        #vert_coord_list = vert_data_raw.split()
        vcl = vert_data_raw.split()
        new_verts = []
        #the values combined into coordinates
        for idx in range(len(vcl)//3):
            new_verts += [(vcl[idx*3], vcl[idx*3 + 1], vcl[idx*3 + 2])]
        
        #add the coordinates to the data library
        if "Verts" in mesh_data.keys():
            mesh_data["Verts"] += new_verts
        else:
            mesh_data["Verts"] = new_verts
        curpos = found_vert_data[1]

#export the data

#Mesh format is a dictionary
#"Name": string with the mesh name
#"Verts": list of vertexes as three float tuples (x, y, z)
#"Faces": list of faces, tuple of absolute vertex indexes
#"DataPosition": position in the original file data where the mesh begins

Header = '''# Paul Spooner .mu Convertor v0.1
# www.peripheralarbor.com
'''

Object_Marker = "o "

Vertex_Marker = "v "

Seperator_of_Some_Kind = "s off\n"

Face_Marker = "f "

#initialize output
output = Header

for mesh_data in mesh_list:
    #only export meshes that have vertex data
    if "Verts" in mesh_data.keys():
        #add the name first
        output += Object_Marker + mesh_data["Name"] + "\n"
        #add the vertexes
        for vertex in mesh_data["Verts"]:
            output += Vertex_Marker + " ".join(vertex) + "\n"
    else: continue
    if "Faces" in mesh_data.keys():
        #I don't know what this seperator is, but here you go
        output += Seperator_of_Some_Kind
        #I don't know how to make faces either
        output += Face_Marker + " 1 2 3 4" + " \n"
        

#output = "no meaningful output yet"

f = open(fileout, 'w')
f.write(output)
f.close()
