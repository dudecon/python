# Document parsing script
# For cleanup of GVK_Source.txt

filein = 'GVK_Source.txt'
#filein = "test.txt"
fileout = 'GVK_Result.txt'
#fileout = 'testproduct.txt'

#start_tag = '<span class="GramE">'
#start_tag = '<span style="mso-spacerun:yes">'

strings_to_replace = [(",",""),
                      ("<tbody>",""),
                      ("    </tbody>",""),
                      ("        <tr>\n",""),
                      ("\n            </td>\n",","),
                      ("            <td >\n            ",""),
                      ("        </tr>",""),
                      ("            ",""),
                      ]

#open the file and read it into memory as "data"
f = open(filein, 'r')
data = f.read()
f.close()

#print(data[:50])
for pair in strings_to_replace:
    start_tag = pair[0]
    end_tag = pair[1]
    while True:
        #parse looking for keyphrase
        start_pos = data.find(start_tag)
        #print(start_pos)
        #loop until end of file reached
        if start_pos == -1: break
        #parse looking for end keyphrase
        # remove just the start tag
        # replace it with the end tag
        cut_start = start_pos
        cut_end = start_pos + len(start_tag)
        data = data[:cut_start] + end_tag + data[cut_end:]

#save the file out
f = open(fileout, 'w')
f.write(data)
f.close()
