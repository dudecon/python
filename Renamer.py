# Rename files to add "_"
# change to "renames" to create directories, separate with '/'

from os import rename, listdir

thesefiles = listdir()
target = "Prefix"
tlen = len(target)
for f in thesefiles:
    if f[:tlen] == target:
        n = f
        n = n[:tlen] + '_' + n[tlen:]
        rename(f, n)
        print(n)