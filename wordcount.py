# Document parsing script
# count up the number of words of each type

from collections import OrderedDict

filein = 'ffts_ps.html'
#filein = "test.txt"
fileout = 'wordcount.txt'
#fileout = 'testproduct.txt'

#number of characters to compare for each word
comp_len = 5

#open the file and read it into memory as "data"
'''f = open(filein, 'r')
data = f.read()
f.close()'''
data = '''Placeholder'''
#print(data[:50])

#clean out anything between brackets, replace with whitespace
print("removing newlines")
data = data.replace('\n',' ')
print("Removing tags")
curpos = 0
while True:
    #parse looking for keyphrase
    found_pos = data.find('<', curpos)
    #print(found_pos)
    #loop until end of file reached
    if found_pos == -1:
        break
    #parse looking for end keyphrase
    end_pos = data.find('>', found_pos)
    #print(end_pos)
    if end_pos == -1:
        print("no close tag found, abort")
        break
    
    # remove the whole tag, but not the tagged text
    # Do this to the whole dataset, since tags are likely to repeat
    cut_string = data[found_pos:end_pos+1]
    #print(cut_string)
    data = data.replace(cut_string, "")
    #data = data[:cut_start] + ' ' + data[cut_end:]
    curpos = found_pos + 1

print("Removing Punctuation!")
#remove all punctuation
for character in '''"”“'’‘,;:.·()!?-*–%''':
    data = data.replace(character, '')

#print(data)
word_count = {}
all_words = data.split()
full_len = len(all_words)
print(full_len, "words")
# count all the words
print("Counting the words")
for word in all_words:
    search_word = word
    #uniform case
    search_word = search_word.capitalize()
    #trim plurality and posession from longer words
    if len(search_word) > 3:
        search_word = search_word.rstrip("s'’‘")
    #trim long words
    if len(search_word) > comp_len:
        search_word = search_word[:comp_len]
    #if nothing is left, continue
    if search_word == '': continue
    #increment the word count
    if search_word in word_count.keys():
        word_count[search_word] += 1
    else:
        word_count[search_word] = 1

print(len(word_count), "unique")

#sort the counts
word_list = OrderedDict(sorted(word_count.items(), key=lambda t: t[1], reverse=True))

#print(word_list.items())

#print it nicely

output = "A total of {} words were parsed,\n".format(full_len)
output += "of which {} were identified as unique.\n".format(len(word_count))
output += "Only the initial {} characters were considered.\n\n".format(comp_len)
output += ("       qty :  {:<" + str(comp_len) + "}  : ppm\n\n").format("word")
for datapair in word_list.items():
    #print(datapair[1], " : ", datapair[0])
    fraction = (datapair[1] / full_len) * 1000000
    output += ("{:>10,} :  {:<" + str(comp_len) + "}  : {:.2f}\n").format(datapair[1], datapair[0], fraction)
    #output += " %\n"



#save the file out
f = open(fileout, 'w')
f.write(output)
f.close()

print("done!")
