# Faith Wedding Round Text Label Generator
# Outputs T2 Laser .t2s sketch files

# dimensions appear to be in mm
# from bottom-left corner
x = 40
y = 40
FirstLine = f"T2Laser Sketch v2,{x},{y}\n"
SecondLine = "X/,0/,0/,0/,0/,0/,0/,0{|}0{|}0\n"
# text line format
# T/,X/,Y/,TEXT/,FONT/,SIZE/,(0 for left aligned, 1 for centered)/,0{|}ROTATION{|}0

# for a 40 width panel, ~11 is the most for 12pt chars
# <=4 for 20pt
# ~5  for 18pt
# ~6  for 16pt
# ~7  for 14pt
# ~8  for 12pt
# ~10 for 11pt
# ~12 for 10pt
# ~14 for 9.5pt
# ~15 for 8.5pt
# ~16 for 8pt
# ~17 for 7.5pt
# ~19 for 7pt
# ~20 for 6.5pt
# ~21 for 6pt
# ~23 for 5.5pt
# ~26 for 5pt
# ~29 for 4.5pt
# ~32 for 4pt

def fontsize(text):
    txtln = len(text)
    fontsizelookup = (20,23,22,21,20,18,16,14,12,11,11,10,9.5,9,9,8.5,8,7.5,7,7,6.5,6,5.5,5.5,5,5,5,4.5,4.5,4.5,4)
    lookuplen = len(fontsizelookup)
    if txtln >= lookuplen:
        return fontsizelookup[-1]
    else:
        return fontsizelookup[txtln]

tptxt = "Ah;"
bttxt = "The semicolon."
tpsz = fontsize(tptxt)
btsz = fontsize(bttxt)
TopTextLine =    f"T/,19/,8/,{tptxt}/,Edwardian Script ITC/,{tpsz}" + "/,1/,0{|}0{|}0\n"
BottomTextLine = f"T/,19/,20/,{bttxt}/,Edwardian Script ITC/,{btsz}" + "/,1/,0{|}0{|}0\n"

f = open(f"{tptxt} {bttxt} edwd.t2s",'w')
f.write(FirstLine)
f.write(SecondLine)
if len(tptxt): f.write(TopTextLine)
if len(bttxt): f.write(BottomTextLine)
f.close()
