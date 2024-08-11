# Search all the text files, loosely, with a scored search

from os import listdir, path, chdir

wordstofind = ("faith","might")
target = ".txt"

dir_path = path.dirname(path.realpath(__file__))
chdir(dir_path)
thesefiles = listdir()
tlen = len(target)

def scoreword(

def loosefind(text, searchwords, threshhold=115, hitscore=100, partialpenalty=1.618):
    '''returns a sorted list of all the text that scores above the threshhold'''
    title = text.split(sep="\n")[0].strip()
    anyfound = False
    for word in searchwords:
        if word in text:
            anyfound = True
    if not anyfound:
        #print(f"--- no words found in:\n-   {title}   -")
        return
    #print(f"--- found the words in ---\n-   {title}   -")
    splittext = text.split()
    score = 0
    for textword in splittext:
        wordscore = 0
        


targlen = len(target)

for fnm in thesefiles:
    if fnm[-targlen:] == target:
        f = open(fnm, encoding="utf-8")
        contents = f.read()
        f.close()
        loosefind(contents, wordstofind)
