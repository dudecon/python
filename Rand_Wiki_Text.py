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

DELAYFACTOR = 0.0035

import urllib.request
from random import choice
from time import sleep

try:
    f = open(SAVEFILE, 'r')
    raw = f.readline()
    f.close()
    rem_pgs = eval(raw)
except:  # rebuild the list
    rem_pgs = []
    from urllib.request import urlopen

    with urlopen(URL) as f:
        html = f.read()
    # second place you get 'class="hlist"'
    cursor = html.find(b'class="hlist"')
    cursor = html.find(b'class="hlist"', cursor + 1)
    # then make a list of all the html links
    sstr = b'<a href="'
    offset = len(sstr)
    cursor = html.find(sstr, cursor) + offset
    while cursor > offset:
        end = html.find(b'"', cursor)
        page = str(html[cursor:end])[2:-1]
        if page[:6] != '/wiki/': break
        if page.find('User:') > 0: break
        if page.find('Help:') > 0: break
        if page.find('Category:') > 0: break
        page = page[6:]
        rem_pgs.append(page)
        cursor = html.find(sstr, end) + offset


def tgx(st, strt, endt):
    while True:
        stpos = st.find(strt)
        if stpos == -1: break
        edpos = st.find(endt, stpos)
        if edpos == -1: break
        edpos += len(endt)
        st = st[:stpos] + st[edpos:]
    return st


def cln(st):
    precull = ('\t',)
    excice = ('head', 'script', 'footer', 'sup', 'noscript', 'nav', 'form', 'cite', 'ol',
              'semantics', 'math')
    detag = ('html', 'div', 'body', '!DOCTYPE', 'a', '!--', 'img', 'style',
             'li', 'td', 'ul', 'tr', 'tbody', 'table', 'h1', 'h2', 'h3', 'h4',
             'span', 'th', 'p', 'i', 'b', 'small', 'label', 'dd', 'dl', 'dt', 'blockquote',
             'center',)
    postcull = ('</abbr>', '[edit]')
    replacement = (('\n\n', '\n'), ('&lt;', '<'), ('&gt;', '>'), ('&amp;', '&'),
                   ('&euro;', '€'), ('&pound;', '£'), ('&quot;', '"'), ('&apos;', "'"),
                   ('&nbsp;', ' '), ('&ensp;', ' '), ('&emsp;', ' '), ('&emsp13;', ' '),
                   ('&numsp;', ' '), ('&puncsp;', ' '), ('&thinsp;', ' '), ('&hairsp;', ' '),
                   )
    for tg in precull:
        st = st.replace(tg, '')
    for tg in excice:
        strt = f'<{tg}'
        endt = f'</{tg}>'
        st = tgx(st, strt, endt)
    st = tgx(st, '<style data', '</style>')
    for tg in detag:
        st = tgx(st, f'<{tg}', '>')
        st = st.replace(f'</{tg}>', '')
    for tg in postcull:
        st = st.replace(tg, '')
    for (rpl1, rpl2) in replacement:
        while rpl1 in st:
            st = st.replace(rpl1, rpl2)
    return st


while True:
    if len(rem_pgs) == 0:
        break
    idx = choice(range(len(rem_pgs)))
    chosen_page = rem_pgs[idx]
    # chosen_page = 'Atlanersa'
    with urllib.request.urlopen(SITE + chosen_page) as response:
        html = response.read()
    page = html.decode("utf-8")
    page = cln(page)
    print('\n\n')
    for ln in page.split('\n'):
        ln = ln.strip()
        if len(ln) == 0: continue
        for thing in ln.split(' '):
            print(thing, end=' ', flush=True)
            sleep(DELAYFACTOR)
        print('')  # for the newline
        sleep((len(ln) + 127) * DELAYFACTOR)
