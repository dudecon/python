# Rand_Wiki.py Version 1.1
# The site to query
SITE = "https://en.wikipedia.org/wiki/"
# the page on the site to query
URL = SITE + "Wikipedia:Featured_articles"
# note that if you want to change either of these, you'll probably
# have to update the parsing code in the "except" below
SAVEFILE = 'wiki_pages.txt'

# Version History
# V 1   2021-08-01  Released
# V 1.1 2021-08-02  Fixed a couple small functionality problems

import webbrowser
from random import choice

try:
    f = open(SAVEFILE,'r')
    raw = f.readline()
    f.close()
    rem_pgs = eval(raw)
except: #rebuild the list
    rem_pgs = []
    from urllib.request import urlopen
    with urlopen(URL) as f: html = f.read()
    #second place you get 'class="hlist"'
    cursor = html.find(b'class="hlist"')
    cursor = html.find(b'class="hlist"',cursor+1)
    # then make a list of all the html links
    sstr = b'<a href="'
    offset = len(sstr)
    cursor = html.find(sstr,cursor) + offset
    while cursor > offset:
        end = html.find(b'"',cursor)
        page = str(html[cursor:end])[2:-1]
        if page[:6] != '/wiki/': break
        if page.find('User:') > 0: break
        if page.find('Help:') > 0: break
        if page.find('Category:') > 0: break
        page = page[6:]
        rem_pgs.append(page)
        cursor = html.find(sstr,end) + offset
 
inchoice = "?"
while True:
    if len(rem_pgs) == 0:
        input("There are no more pages. Press return to close.")
        break
    printflag = False
    if len(inchoice)!= 0:
        inchoice = inchoice.lower()
        initial = inchoice[0]
        if initial == 's':
            print("Saving")
            f = open(SAVEFILE,'w')
            f.write(str(rem_pgs))
            f.close()
            if inchoice == 'sc': break
            else: print('{} pages left'.format(len(rem_pgs)))
            inchoice = input('Saved: ')
            continue
        elif initial == 'p':
            print(rem_pgs)
            inchoice = input('Those are the currently loaded remaining pages :')
            continue
        elif inchoice[-1] == '?':
            print('{} pages left'.format(len(rem_pgs)))
            print('Enter to bring up a Featured Wikipedia page\n"s" to save, "sc" to save and close, "p" to print')
            inchoice = input('What would you like to do: ')
            continue
    idx = choice(range(len(rem_pgs)))
    chosen_page = rem_pgs.pop(idx)
    webbrowser.open(SITE + chosen_page)
    inchoice = input('Page {} queued: '.format(chosen_page))
 
