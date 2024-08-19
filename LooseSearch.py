# Search all the text files, loosely, with a scored search

from os import listdir, path, chdir

scoremultiplier = 1.618
PRINTMARGIN = 20
THRSHLD = 40

wordstofind = {"power":12, "riches":12, "thanksgiving":8, "wisdom":6,
               "strength":12, "might":12, "thank":3,
               "honor":12, "glory":12, "majesty":6, "blessing":12,
               'seven':7}
target = ".txt"

dir_path = path.dirname(path.realpath(__file__))
chdir(dir_path)
thesefiles = listdir()
tlen = len(target)

def scoreword(rawwordtext, searchwords, partialpenalty=1.618):
    '''return the float value for the word score'''
    wordtext = rawwordtext.lower()
    for c in ('"',"'",',','.','!','?',';',':','“','”'):
        wordtext = wordtext.replace(c,'')
    #if wordtext != rawwordtext: print(wordtext, rawwordtext)
    baselen = len(wordtext)
    totalscore = 0
    for word in searchwords:
        word_score = 0
        if word in wordtext:
            penalty = (len(word)/baselen)**partialpenalty
            word_score = searchwords[word] * penalty
        elif False:#wordtext in word:
            penalty = (baselen/len(word))**partialpenalty
            word_score = searchwords[word] * penalty
        totalscore += word_score
    return totalscore * scoremultiplier


def loosefind(text, searchwords, threshhold=115, partialpenalty=1.618):
    '''returns a sorted list of all the text that scores above the threshhold'''
    splittext = text.split()
    score = 0
    found = False
    begin = 0
    end = 0
    pairs = []
    topscore = 0
    for i, textword in enumerate(splittext):
        word_score = scoreword(textword, searchwords)
        #if 90 > word_score > 10: print(word_score,textword,searchwords)
        score += word_score
        if score >= threshhold:
            topscore = max(topscore,score)
            if not found:
                newbegin = max(0,int(i-score+threshhold))
                if len(pairs):
                    if pairs[-1][2] >= newbegin:
                        oldtopscore,begin,end = pairs.pop()
                        topscore = max(topscore,oldtopscore)
                        found = True
                if not found:
                    begin = newbegin
                    found = True
        else:
            if found:
                end = i
                pairs.append((topscore,begin,end))
                topscore = 0
                found = False
        score = max(0,score-1)
    pairs.sort(reverse=True)
    return pairs


targlen = len(target)

for fnm in thesefiles:
    if fnm[-targlen:] == target:
        f = open(fnm, encoding="utf-8")
        contents = f.read()
        f.close()
        foundsections = loosefind(contents, wordstofind, THRSHLD)
        if len(foundsections):
            title = contents.split(sep="\n")[0].strip()
            print(title)
            splittext = contents.split()
            for section in foundsections:
                begin = max(section[1]-PRINTMARGIN,0)
                end = section[2]+PRINTMARGIN
                print("\n",section,' '.join(splittext[begin:end]))
