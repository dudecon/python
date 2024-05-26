# Rand_Wiki_Text.py Version 0.1
# prints out wikipedia featured article text
# The site to query
SITE = "https://en.wikipedia.org/wiki/"
# the page on the site to query
URL = SITE + "Wikipedia:Featured_articles"
# note that if you want to change either of these, you'll probably
# have to update the parsing code in the "except" below
SAVEFILE = 'wiki_pages.txt'

# Version History
# V 0.1 2021-11-29  Worked on it
# V 0.2 2024-05-25  Libraries and better cleaning


import urllib.request
from urllib.request import urlopen
from random import choice
from time import sleep
from SlowPrint import sprint
from HTML_Cleaner import *

DEBUG = False

def prepWiki(rawhtm):
    garbage_starts = rawhtm.find('See also</span>')
    if garbage_starts > 1000:
        rawhtm = rawhtm[:garbage_starts]
    pre_excise = ('a class="mw-jump-link"', 'table class="infobox',
                  'table class="sidebar')
    for tg in pre_excise:
        rawhtm = excise_content(rawhtm, tg)
    return rawhtm

def get_clean_wiki_page(page_name):
    with urllib.request.urlopen(SITE + page_name) as response:
        wikihtm = response.read()
    page = wikihtm.decode("utf-8")
    page = prepWiki(page)
    page = cln(page)
    return page

if __name__ == '__main__':
    try:
        f = open(SAVEFILE, 'r')
        raw = f.readline()
        f.close()
        rem_pgs = eval(raw)
    except:  # rebuild the list
        rem_pgs = []
        from urllib.request import urlopen

        with urlopen(URL) as f:
            featuredhtm = f.read()
        # second place you get 'class="hlist"'
        cursor = featuredhtm.find(b'class="hlist"')
        cursor = featuredhtm.find(b'class="hlist"', cursor + 1)
        # then make a list of all the html links
        sstr = b'<a href="'
        offset = len(sstr)
        cursor = featuredhtm.find(sstr, cursor) + offset
        while cursor > offset:
            end = featuredhtm.find(b'"', cursor)
            page = str(featuredhtm[cursor:end])[2:-1]
            if page[:6] != '/wiki/': break
            if page.find('User:') > 0: break
            if page.find('Help:') > 0: break
            if page.find('Category:') > 0: break
            page = page[6:]
            rem_pgs.append(page)
            cursor = featuredhtm.find(sstr, end) + offset
        
    while True:
        if len(rem_pgs) == 0:
            break
        idx = choice(range(len(rem_pgs)))
        chosen_page = rem_pgs[idx]
        #chosen_page = 'Atlanersa'
        print('\n\n')
        sprint(get_clean_wiki_page(chosen_page))
