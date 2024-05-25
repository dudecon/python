# Python thingies for website gallery page setup
from random import choice
bordcolplt = (0,1,1,2)
bordcolbs = [0,0,0]
for i in range(len(bordcolbs)): bordcolbs[i] = choice(bordcolplt)
bordofstplt = (-1,0,0,1,1)
#bordcolbs = [1,1,1]
TitleText = "David Moore Wedding".strip()
PGWDTH = "800"
WDOP = f"width:{PGWDTH}px; "
#WDOP = ""
BRDOPBS= "border: 3px solid"

DESCRIPTION = """Placeholder"""
Image_raw_text = '''
C:/Users/dudec/Pictures/High_Bookshelf/Midjourney/Laser_Decoration_Design_1.jpg
C:/Users/dudec/Pictures/High_Bookshelf/Midjourney/Laser_Decoration_Design_2.jpg
C:/Users/dudec/Pictures/High_Bookshelf/Midjourney/Laser_Decoration_Design_3.jpg
C:/Users/dudec/Pictures/High_Bookshelf/Midjourney/Laser_Decoration_Design_4.jpg
C:/Users/dudec/Pictures/High_Bookshelf/Midjourney/Laser_Decoration_Design_5.jpg
C:/Users/dudec/Pictures/High_Bookshelf/Midjourney/Laser_Decoration_Design_6.jpg
C:/Users/dudec/Pictures/High_Bookshelf/Midjourney/Laser_Decoration_Design_7.jpg
C:/Users/dudec/Pictures/High_Bookshelf/Midjourney/Laser_Decoration_Design_8.jpg
C:/Users/dudec/Pictures/High_Bookshelf/Midjourney/Laser_Decoration_Design_9.jpg
C:/Users/dudec/Pictures/High_Bookshelf/Midjourney/Laser_Decoration_Design_10.jpg
C:/Users/dudec/Pictures/High_Bookshelf/Midjourney/Laser_Decoration_Design_11.jpg
C:/Users/dudec/Pictures/High_Bookshelf/Midjourney/Laser_Decoration_Design_12.jpg
C:/Users/dudec/Pictures/High_Bookshelf/Midjourney/Laser_Decoration_Design_13.jpg
C:/Users/dudec/Pictures/High_Bookshelf/Midjourney/Laser_Decoration_Design_14.jpg
C:/Users/dudec/Pictures/High_Bookshelf/Midjourney/Laser_Decoration_Design_15.jpg
C:/Users/dudec/Pictures/High_Bookshelf/Midjourney/Laser_Decoration_Design_16.jpg
C:/Users/dudec/Pictures/High_Bookshelf/Midjourney/Laser_Decoration_Design_17.jpg
C:/Users/dudec/Pictures/High_Bookshelf/Midjourney/Laser_Decoration_Design_18.jpg
C:/Users/dudec/Pictures/High_Bookshelf/Midjourney/Laser_Decoration_Design_19.jpg
C:/Users/dudec/Pictures/High_Bookshelf/Midjourney/Laser_Decoration_Design_20.jpg
C:/Users/dudec/Pictures/High_Bookshelf/Midjourney/Laser_Decoration_Design_21.jpg
C:/Users/dudec/Pictures/High_Bookshelf/Midjourney/Laser_Decoration_Design_22.jpg
C:/Users/dudec/Pictures/High_Bookshelf/Midjourney/Laser_Decoration_Design_23.jpg
C:/Users/dudec/Pictures/High_Bookshelf/Midjourney/Laser_Decoration_Design_24.jpg
'''

PARENTCAT = "Life"

DESCRIPTION = DESCRIPTION.strip().replace("\n\n","\n<br>")
Image_raw_text = Image_raw_text.strip()

folders = [l.split()[0] for l in Image_raw_text.split(sep='\n') if l.split()[0][-1] == '/']
images  = [l.split()[0].split(sep='/')[-1] for l in Image_raw_text.split(sep='\n') if l.split()[0][-1] != '/']
#dates   = [l.split()[1] for l in Image_raw_text.split(sep='\n') if l.split()[0][-1] != '/']
# use the below for files pasted from the local drive
#images = [l.split(sep='/')[-1] for l in Image_raw_text.split(sep='\n')]

BGColor = ""
R = 0xf2
G = 0xf2
B = 0xf2
chan = [R,G,B]
offsets = [-30, -10, -8, -4, 4, 8, 13]
for col in chan:
    off = choice(offsets)
    BGColor += hex(col + off)[2:]
    offsets.remove(off)
#BGColor = "d2d2d2"

Header = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<title>{TitleText}</title>
<link rel="stylesheet" type="text/css" href="/style.css" />
</head>
<body style="background-color: #{BGColor};
	color: #222222;
	font-family: monospace, Sans-serif;
	font-size: 14px;
	cursor:default;">

<div style="opacity: .2; z-index: 1;"><div style="position: absolute;">
<img width="300" alt="Index Picture, left" height="970" src="/PeripheraLeft.png" border="0" style="float: left; margin-top: 50px;" /></div>
<div style="position: absolute; width: 100%;">
<img width="300" alt="Index Picture, right" height="970" src="/PeripheraLight.png" border="0" style="float: right; margin-top: 50px;" /></div>
</div>
<div style="width: {PGWDTH}px; margin: auto; position: relative; z-index: 2;">

'''

Title = f'''<h2>{TitleText}</h2>
<p>{DESCRIPTION}
</p> 
<p>I occasionally do <a href="http://handyman.tryop.com/">handyman work</a> along with other <a href="http://tryop.com/products/">physical products</a>. If you'd like to <a href="/commission/">commission a custom build</a>, I can help you with that.</p>
<h3></h3>
'''

def description(instr):
    outstr = instr.strip("0123456789_")
    uppercount = 0
    space_inserts = []
    for ch in enumerate(outstr):
        if ch[1].isupper():
            uppercount += 1
        else:
            uppercount = 0
        if ch[0] == 0: continue
        if uppercount == 1: space_inserts.append(ch[0])
    space_inserts.sort(reverse=True)
    for i in space_inserts:
        outstr = outstr[:i] + ' ' + outstr[i:]
    outstr = outstr.replace("_","")
    return outstr

Output_HTML = Header + Title
for fld in folders:
    desc = description(fld[:-1])
    Output_HTML += f'''<a href="{fld}"><h3>{desc}</h3></a>
    <p></p>
'''

if len(images) and len(folders): Output_HTML += "<h3>Images</h3>\n"
for img in images:
    imgname = ''.join(img.split(sep='.')[:-1])
    imgdsc = description(imgname)
    #imgdsc = "Clouds"
    BRDOP = ""
    for i in range(len(bordcolbs)): BRDOP += str(max(bordcolbs[i] + choice(bordofstplt), 0))
    BRDOP = f"{BRDOPBS} #{BRDOP};"
    Output_HTML += f'''<p id="{imgname}">{imgdsc}
    <br><img src="{img}" style="{WDOP}{BRDOP}" title="{imgdsc}"/></p>
'''

Footer = f'''

<h2>Navigation Links</h2>
<a href="../"><h3>Level Up to {PARENTCAT}</h3></a>
<a href="/gallery/"><h3>Gallery Root</h3></a>
<a title="Back to PeripheralArbor" href="/"><h3>Back to Peripheral Arbor Homepage</h3></a>
</div>
</body>
</html>'''

Output_HTML += Footer
f = open("index.htm", 'w')
f.write(Output_HTML)
f.close()
