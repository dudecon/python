from os import rename, listdir
from PIL import Image

thesefiles = listdir()
target = ".png"
new = ".jpg"
newdir = "./PNGs/"
tlen = len(target)
for f in thesefiles:
    if f[-tlen:] == target:
        image = Image.open(f)
        image = image.convert('RGB')
        n = f
        n = n[:-tlen] + new
        image.save(n)
        m = newdir + f
        rename(f, m)
        print("processed", f)