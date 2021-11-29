# Document parsing script
# For cleanup of ffts_ps.html

filein = 'ffts_ps.html'
#filein = "test.txt"
fileout = 'ffts_ps.html'
#fileout = 'testproduct.txt'

#start_tag = '<span class="GramE">'
#start_tag = '<span style="mso-spacerun:yes">'
start_tag = ' </p>'

#end_tag = '</span>'
end_tag = '</p>'


#open the file and read it into memory as "data"
f = open(filein, 'r')
data = f.read()
f.close()

#print(data[:50])
while True:
    #parse looking for keyphrase
    start_pos = data.find(start_tag)
    #print(start_pos)
    #loop until end of file reached
    if start_pos == -1: break
    #parse looking for end keyphrase
    '''end_pos = data.find(end_tag, start_pos)
    #print(end_pos)
    if end_pos == -1:
        print("no close tag found, abort")
        break'''
    '''
    # remove the last first
    # this preserves the position data
    cut_start = end_pos
    cut_end = cut_start + len(end_tag)
    data = data[:cut_start] + data[cut_end:]
    #then remove the first
    cut_start = start_pos
    cut_end = cut_start + len(start_tag)
    data = data[:cut_start] + data[cut_end:]
    '''
    '''
    # remove the whole tag and anything inbetween
    # replace it with a single space
    cut_start = start_pos
    cut_end = end_pos + len(end_tag)
    data = data[:cut_start] + ' ' + data[cut_end:]
    '''
    # remove just the start tag
    # replace it with the end tag
    cut_start = start_pos
    cut_end = start_pos + len(start_tag)
    data = data[:cut_start] + end_tag + data[cut_end:]

#save the file out
f = open(fileout, 'w')
f.write(data)
f.close()
