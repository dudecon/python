# Python thingies for website gallery page setup
from random import choice
from os import listdir, startfile, path, chdir
import subprocess, platform

def osopen(filepath):
    '''Opens the file with whatever the default OS software is'''
    if platform.system() == 'Darwin':       # macOS
        subprocess.call(('open', filepath))
    elif platform.system() == 'Windows':    # Windows
        startfile(filepath)
    else:                                   # linux variants
        subprocess.call(('xdg-open', filepath))

# Used to generate text files, and check for un-populated text
placeholder = u'''This is placeholder text. Please replace all of this with the story of "{}".
If you prefer to talk instead of type, press ⊞ + H (hold the windows key and press H) to activate speech-to-text in Windows.
Don't forget to save your changes to this file!

If this keeps bringing up the same image, it's because you haven't deleted this boilerplate text yet.

'''
checktext = placeholder[:40]

def process_files():
    dir_path = path.dirname(path.realpath(__file__))
    chdir(dir_path)
    thesefiles = listdir()
    image_extensions = ("png","jpg","jpeg","gif","tiff","webp","bmp")

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

    for img in image_file_names:
        if img not in text_file_names:
            content = placeholder.format(img)
            f = open(img + ".txt", 'w', encoding='utf-8')
            f.write(content)
            f.close()

    # we don't want these hanging around
    # delete so we don't accidentally reference them
    del(image_file_names)
    del(text_file_list)
    del(text_file_names)
    return(image_file_list)

descriptions = {}
# check for unpopulated text files
def AllDescriptionsPopulated(image_file_list):
    for imgf in image_file_list:
        name = '.'.join(imgf.split('.')[:-1])
        txtf =  name + '.txt'
        f = open(txtf, 'r', encoding='utf-8')
        content = f.read()
        f.close()
        if checktext in content:
            osopen(imgf)
            osopen(txtf)
            return(False)
        else:
            descriptions[imgf] = content
    return(True)


def photo_title():
    templates = [
        "My {emotion} {noun}",
        "{emotion} Memories",
        "A {emotion} Moment",
        "{emotion} {noun}",
        "Our {emotion} {noun}",
        "Cherished {noun}",
        "Timeless {noun}",
        "A {emotion} {noun}",
        "{emotion} Times"
    ]
    
    emotions = [
        'Poignant', 'Beloved', 'Joyful', 'Bittersweet', 'Nostalgic', 'Heartwarming',
        'Delightful', 'Cherished', 'Memorable', 'Wonderful', 'Magical', 'Precious'
    ]
    
    nouns = [
        'Photo', 'Moment', 'Time', 'Adventure', 'Experience', 'Memory', 'Journey', 
        'Story', 'Capture', 'Event', 'Occasion'
    ]
    
    template = choice(templates)
    emotion = choice(emotions)
    noun = choice(nouns)
    
    return template.format(emotion=emotion, noun=noun)

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
    outstr = outstr.replace("_"," ")
    outstr = outstr.replace("."," ")
    while "  " in outstr:
        outstr = outstr.replace("  "," ")
    if len(outstr) < len(instr)/3:
        outstr = photo_title()
    return outstr


def MakePage(images, html_page_name = "index.htm"):
    bordcolplt = (0,1,1,2)
    bordcolbs = [0,0,0]
    for i in range(len(bordcolbs)): bordcolbs[i] = choice(bordcolplt)
    bordofstplt = (-1,0,0,1,1)
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

    <h4>Made with Photo Stories</h4>
    <p style="font-size: 8px;">This photo page was made using the free and open source
    <a href="https://github.com/dudecon/python/blob/main/PhotoStories.py">Photo Stories</a> tool. If you would like to support
    the development of this software, <a href="https://paypal.me/PaulSpooner">click here</a>. Thanks for your
    support, and God bless.</p>
    </div>
    </body>
    </html>'''

    Output_HTML += Footer
    f = open(html_page_name, 'w', encoding='utf-8')
    f.write(Output_HTML)
    f.close()

if __name__ == '__main__':
    img_files = process_files()
    if AllDescriptionsPopulated(img_files):
        page_name = "index.htm"
        MakePage(img_files, page_name)
        osopen(page_name)
