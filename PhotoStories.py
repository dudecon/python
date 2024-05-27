# Python thingies for website gallery page setup
from random import choice
from os import listdir, startfile, path, chdir
import subprocess, platform

def osopen(filepath):
    if platform.system() == 'Darwin':       # macOS
        subprocess.call(('open', filepath))
    elif platform.system() == 'Windows':    # Windows
        startfile(filepath)
    else:                                   # linux variants
        subprocess.call(('xdg-open', filepath))

dir_path = path.dirname(path.realpath(__file__))
chdir(dir_path)
thesefiles = listdir()
image_extensions = ("png","jpg","gif","tiff","webp")

# Make lists of all the images and the text files in the folder
image_file_list = []
text_file_list = []
for f in thesefiles:
    extension = f.split('.')[-1].lower()
    if extension in image_extensions:
        image_file_list.append(f)
    elif extension == 'txt':
        text_file_list.append(f)

image_file_names = ['.'.join(img.split('.')[:-1]) for img in image_file_list]
text_file_names  = ['.'.join(txt.split('.')[:-1]) for txt in  text_file_list]


# If missing, generate text files
placeholder = '''This is placeholder text. Please replace all of this with the story of "{}".
Don't forget to save your changes to this file!'''
checktext = placeholder[:40]

for img in image_file_names:
    if img not in text_file_names:
        content = placeholder.format(img)
        f = open(img + ".txt",'w')
        f.write(content)
        f.close()
        text_file_names.append(img)
        text_file_list.append(img + ".txt")
    
'''print(image_file_list)
print(image_file_names)
print(text_file_list)
print(text_file_names)'''

descriptions = {}
# check for unpopulated text files
def AllDescriptionsPopulated():
    for i, name in enumerate(image_file_list):
        txtf =  text_file_list[i]
        imgf = image_file_list[i]
        f = open(txtf,'r')
        content = f.read()
        f.close()
        if checktext in content:
            osopen(imgf)
            osopen(txtf)
            return(False)
        else:
            descriptions[imgf] = content
    return(True)


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


def MakePage(html_page_name = "index.htm"):
    #folders = [l.split()[0] for l in Image_raw_text.split(sep='\n') if l.split()[0][-1] == '/']
    folders = []
    images  = image_file_list
    #dates   = [l.split()[1] for l in Image_raw_text.split(sep='\n') if l.split()[0][-1] != '/']
    # use the below for files pasted from the local drive
    #images = [l.split(sep='/')[-1] for l in Image_raw_text.split(sep='\n')]

    bordcolplt = (0,1,1,2)
    bordcolbs = [0,0,0]
    for i in range(len(bordcolbs)): bordcolbs[i] = choice(bordcolplt)
    bordofstplt = (-1,0,0,1,1)
    #bordcolbs = [1,1,1]
    TitleText = "Photo Stories".strip()
    DESCRIPTION = TitleText
    PGWDTH = "800"
    WDOP = f"width:{PGWDTH}px; "
    BRDOPBS= "border: 3px solid"

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
    </head>
    <body style="background-color: #{BGColor};
            color: #222222;
            font-family: serif;
            font-size: 14px;
            cursor:default;">

    <div style="width: {PGWDTH}px; margin: auto; position: relative;">

    '''

    Title = f'''<h2>{TitleText}</h2>
    
    '''



    Output_HTML = Header + Title
    for fld in folders:
        desc = description(fld[:-1])
        Output_HTML += f'''<a href="{fld}"><h3>{desc}</h3></a>
        <p></p>
    '''

    if len(images) and len(folders): Output_HTML += "<h3>Images</h3>\n"
    for img in images:
        imgname = ''.join(img.split(sep='.')[:-1])
        imgtitle = description(imgname)
        imgdsc = descriptions[img]
        imgdsc = imgdsc.replace('\n','<br>\n')
        BRDOP = ""
        for i in range(len(bordcolbs)): BRDOP += str(max(bordcolbs[i] + choice(bordofstplt), 0))
        BRDOP = f"{BRDOPBS} #{BRDOP};"
        Output_HTML += f'''<p id="{imgname}">{imgdsc}
        <br><img src="{img}" style="{WDOP}{BRDOP}" title="{imgtitle}"/></p>
    '''

    Footer = f'''

    <h3>Made with Photo Stories</h3>
    <p>This photo memories page was made using the free and open source
    <a href="./">Photo Memories</a> tool. If you would like to support
    the development of this software, <a href="./">click here</a>. Thanks for your
    support, and God bless.</p>
    </div>
    </body>
    </html>'''

    Output_HTML += Footer
    f = open(html_page_name, 'w')
    
    f.write(Output_HTML)
    f.close()

if __name__ == '__main__':
    if AllDescriptionsPopulated():
        page_name = "index.htm"
        MakePage(page_name)
        osopen(page_name)
