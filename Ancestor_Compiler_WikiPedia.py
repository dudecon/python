# Rand_Wiki_Text.py Version 0.1
# prints out wikipedia featured article text
# The site to query
SITE = "https://en.wikipedia.org/wiki/"
# the page on the site to query
ROOT_NAME = "John_Howard,_1st_Duke_of_Norfolk"
URL = SITE + ROOT_NAME
DEPTH = 0
# note that if you want to change either of these, you'll probably
# have to update the parsing code in the "except" below
PLAIN_NAME = ROOT_NAME.replace("_"," ")
CLEAN_NAME = PLAIN_NAME.replace(",","")
SAVEFILE = F'Pedigree_{CLEAN_NAME}.txt'

# Version History
# V 0.1 2021-11-29  Worked on it


from urllib.request import urlopen

def tgx(st, strt, endt):
    while True:
        stpos = st.find(strt)
        if stpos == -1: break
        edpos = st.find(endt, stpos)
        if edpos == -1: break
        edpos += len(endt)
        st = st[:stpos] + st[edpos:]
    return st

def tgcts(st, tg):
    strt = f"<{tg}"
    endg = f"</{tg}>"
    stpos = st.find(strt)
    if stpos == -1: return ""
    edpos = st.find(endt, stpos)
    if edpos == -1: return ""
    stpos = st.find(">", stpos)
    substr = st[1+stpos:edpos]
    return substr,

def cln(st):
    precull = ('\t', )
    excice = ('head', 'script', 'footer', 'sup', 'noscript', 'nav', 'form', 'cite', 'ol')
    detag = ('html','div', 'body', '!DOCTYPE', 'a', '!--', 'img', 'style',
             'li', 'td', 'ul', 'tr', 'tbody', 'table', 'h1', 'h2', 'h3', 'h4',
             'span', 'th', 'p', 'i', 'b', 'small', 'label', 'dd', 'dl', 'dt', 'blockquote',
             'center', )
    postcull = ('</abbr>', '[edit]')
    replacement = (('\n\n','\n'), ('&lt;','<'), ('&gt;','>'), ('&amp;','&'), 
    ('&euro;','€'), ('&pound;','£'), ('&quot;','"'), ('&apos;',"'"), 
    ('&nbsp;',' '), ('&ensp;',' '), ('&emsp;',' '), ('&emsp13;',' '), 
    ('&numsp;',' '), ('&puncsp;',' '), ('&thinsp;',' '), ('&hairsp;',' '), 
    )
    for tg in precull:
        st = st.replace(tg,'')
    for tg in excice:
        strt = f'<{tg}'
        endt = f'</{tg}>'
        st = tgx(st, strt, endt)
    st = tgx(st, '<style data', '</style>')
    for tg in detag:
        st = tgx(st, f'<{tg}', '>')
        st = st.replace(f'</{tg}>', '')
    for tg in postcull:
        st = st.replace(tg,'')
    for (rpl1, rpl2) in replacement:
        while rpl1 in st:
            st = st.replace(rpl1,rpl2)
    return st

def getwikiperson(URL):
    with urlopen(URL) as f: html = f.read()
    personinfo = {}
    page = html.decode("utf-8")
    srch = '"infobox-label">Parents</th>'
    loc = page.find(srch)
    tgcts(page, tg)
    return personinfo

def RecurPedigree(d=0, n="", u="", Ped = {}):
    if DEPTH < d:
        return None
    p = getwikiperson(SITE + u)
    if len(p) < 2: return None
    Ped[n] = p
    if "nm_f" in p:
        if "url_f" in p:
            RecurPedigree(d+1, p["nm_f"], p["url_f"], Ped)
    if "nm_m" in p:
        if "url_m" in p:
            RecurPedigree(d+1, p["nm_m"], p["url_m"], Ped)

Total_Pedigree = {}
RecurPedigree(0, PLAIN_NAME, ROOT_NAME, Total_Pedigree)
print(len(Total_Pedigree), "number of people processed")
