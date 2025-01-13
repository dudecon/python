#USCCB Bible Commentary Cull
#for personal use only

from os import listdir, path, chdir, makedirs, rename

def cull_commentary(txt):
    lines = txt.split('\n')
    culled = []
    for l in lines:
        if len(l) < 7:
            culled.append(l)
            continue
        if l[1] == ".": continue
        if l[0] == "*": continue
        culled.append(l)
    return '\n'.join(culled)

def cull_book(settings):
    name = settings[0]
    chaps = settings[1]
    h = get_bible_book(name,chaps)
    fnm = name + ".txt"
    f = open(fnm, mode='w',encoding="utf-8")
    f.write(h)
    f.close()
    print("saved",fnm)

def process_files(files, ext):
    '''Move the originals and save a culled version in the root'''

    bkpdirname = "NAB_With_Commentary"
    bkpdir = f"./{bkpdirname}/"
    if not bkpdirname in files:
        makedirs(bkpdir)

    for f in files:
        if f.endswith(ext):
            with open(f, encoding="utf-8") as file:
                contents = file.read()
            contents = cull_commentary(contents)
            m = bkpdir + f
            rename(f, m)
            fl = open(f, "w",encoding="utf-8")
            fl.write(contents)
            fl.close()

if __name__ == '__main__':
    dir_path = path.dirname(path.realpath(__file__))
    chdir(dir_path)
    all_files = listdir()
    target_extension = ".txt"
    process_files(all_files, target_extension)
