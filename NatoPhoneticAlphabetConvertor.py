# NATO Phonetic Alphabet substituter
NPA = {'A':'Alfa',
       'B':'Bravo',
       'C':'Charlie',
       'D':'Delta',
       'E':'Echo',
       'F':'Foxtrot',
       'G':'Golf',
       'H':'Hotel',
       'I':'India',
       'J':'Juliett',
       'K':'Kilo',
       'L':'Lima',
       'M':'Mike',
       'N':'November',
       'O':'Oscar',
       'P':'Papa',
       'Q':'Quebec',
       'R':'Romeo',
       'S':'Sierra',
       'T':'Tango',
       'U':'Uniform',
       'V':'Victor',
       'W':'Whiskey',
       'X':'Xray',
       'Y':'Yankee',
       'Z':'Zulu',
       '-':'Dash',
       }
s = input("enter the text you want to read off: ")
su = s.upper()
output = []
for i in su:
    try: output += [NPA[i]]
    except: output += [i]
readoff = " ".join(output)
print(readoff)
input("Press enter when done reading:")
