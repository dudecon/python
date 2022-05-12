# tries to remove bad shortcut files
# these are associated with the "Harry potter" links
# but they appear to be self-replicating and can have
# other file names

wsk = b"wscript.exe"
bkk = b"\x00e\x00:\x00V\x00B\x00S\x00c\x00r\x00i\x00p\x00t\x00 \x00t\x00h\x00u\x00m\x00b\x00.\x00d\x00b\x00"
import os
# localfiles = os.listdir()
curpath = "."
erlog = ""

def rcrchk(curpath, baddepth):
    folders = []
    files = []
    foundbad = False
    with os.scandir(curpath) as sd:
        for entry in sd:
            if entry.is_file(): files.append(entry)
            else: folders.append(entry)
    for f in files:
        if f.name[-4:] != ".lnk": continue
        lnkpth = curpath + "\\" + f.name
        lnkf = open(lnkpth, 'rb')
        lnkcts = lnkf.read()
        lnkf.close()
        if (wsk in lnkcts) and (bkk in lnkcts):
            try: os.remove(lnkpth)
            except: erlog += lnkpth + "\n"
            print(lnkpth, " excised")
            foundbad = True
        #else: print(lnkpth, " is clean")
    # don't recurse if there were no bad links in this directory.
    if foundbad:
        baddepth = 2
        #print("links excised in ", curpath)
    else:
        baddepth -= 1
    if baddepth < 1: return
    for f in folders:
        lnkpth = curpath + "\\" + f.name
        #print("checking ", lnkpth)
        rcrchk(lnkpth, baddepth)

#lnkpth = "RemoteTools.ahk - Shortcut.lnk"
#os.remove(lnkpth)
        
rcrchk(curpath, 1)
if len(erlog):
    f = open("denied.txt", "w")
    f.write(erlog)
    f.close()
if "RemoteReceiver.ahk" not in os.listdir(): os.remove("linkcull.py")
