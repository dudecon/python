# Ancestor_Compiler_WikiPedia.py Version 0.1
# Grabs ancestor data from WikiPedia
# The site to query
SITE = "https://en.wikipedia.org/wiki/"
# the page on the site to query
ROOT_NAME = "John_Howard,_1st_Duke_of_Norfolk"
# ROOT_NAME = "Yaroslav_the_Wise"
URL = SITE + ROOT_NAME
DEPTH = 75
# note that if you want to change either of these, you'll probably
# have to update the parsing code in the "except" below
PLAIN_NAME = ROOT_NAME.replace("_"," ")
CLEAN_NAME = PLAIN_NAME.replace(",","")
SAVEFILE = F'Pedigree_{CLEAN_NAME}.txt'
SAVEFILE = "Pedigree_John Howard 1st Duke of Norfolk.txt"



# Version History
# V 0.1 2021-11-29  Worked on it


from urllib.request import urlopen

def tgx(st, strt, endt):
    # excise all text between all occurrances of the tag pairs
    while True:
        stpos = st.find(strt)
        if stpos == -1: break
        edpos = st.find(endt, stpos)
        if edpos == -1: break
        edpos += len(endt)
        st = st[:stpos] + st[edpos:]
    return st

def tgcts(st, tg):
    # return the text enclosed by a tag
    strt = f"<{tg}"
    endt = f"</{tg}>"
    stpos = st.find(strt)
    if stpos == -1: return ""
    edpos = st.find(endt, stpos)
    if edpos == -1: return ""
    stpos = st.find(">", stpos)
    substr = st[1+stpos:edpos]
    return substr

def alltgcts(st, tg):
    # return a list of all the text enclosed by tags
    strt = f"<{tg}"
    endt = f"</{tg}>"
    stpos = st.find(strt)
    allcontents = []
    while stpos != -1:
        edpos = st.find(endt, stpos)
        if edpos == -1: return allcontents
        stpos = st.find(">", stpos)
        substr = st[1+stpos:edpos]
        allcontents.append(substr)
        stpos = st.find(strt, edpos)
    return allcontents

def cln(st):
    # clean out markup elements
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
    PIF = {}
    # placeholder in case the site search fails for some reason
    PIF['nm'] = URL
    try:
        with urlopen(SITE + URL) as f: html = f.read()
    except:
        return PIF
    page = html.decode("utf-8")
    # populate the name field
    srch = 'id="firstHeading"'
    loc = page.find(srch)
    if loc == -1: return PIF
    tg = "h1"
    nametxt = tgcts(page[loc-10:], tg)
    if len(nametxt) == 0: return PIF
    PIF['nm'] = nametxt
    # if we got this far, the URL is good, so let's save that
    PIF['url'] = URL
    # find the infobox
    srch = 'class="infobox vcard"'
    loc = page.find(srch)
    if loc == -1:
        # no infobox! guess we don't have any dates or parents?
        return PIF
    tg = "table"
    infoboxtxt = tgcts(page[loc-10:], tg)
    # now we should be able to just deal with the infobox without
    # worrying about the rest of the page
    # get key dates, birth and death
    anydates = False
    srch = 'infobox-label">Born'
    loc = infoboxtxt.find(srch)
    if loc != -1:
        tg = "td"
        dtatxt = cln(tgcts(infoboxtxt[loc:], tg))
        PIF['b'] = dtatxt
        anydates = True
    srch = 'infobox-label">Died'
    loc = infoboxtxt.find(srch)
    if loc != -1:
        tg = "td"
        dtatxt = cln(tgcts(infoboxtxt[loc:], tg))
        PIF['d'] = dtatxt
        anydates = True
    if False:#anydates:# turns out, I don't like the long names
        # update the name with the dates
        brn = ""
        if 'b' in PIF: brn = PIF['b']
        did = ""
        if 'd' in PIF: did = PIF['d']
        if ((len(brn)>0) and (len(did)>0)):
            PIF['nm'] = PIF['nm'] + f" ({brn} to {did})"
        elif (len(brn)>0):
            PIF['nm'] = PIF['nm'] + f" ({brn})"
        else: PIF['nm'] = PIF['nm'] + f" ({did})"
    # find the parents
    # try Father and Mother first
    def grabname(ptx, pid):
        # print(ptx, pid)
        if (('href="' in ptx) and ("redlink=1" not in ptx)):
            # get the href so we can follow up on the ancestor
            loc = ptx.find(srch)
            urlstart = ptx.find('"', loc+1)+1+6
            urlend = ptx.find('"', urlstart)
            url = ptx[urlstart:urlend]
            PIF[pid] = url
        else:
            name = tgx(ptx, '(', ')')
            name = tgx(name, '<', '>')
            name = name.strip()
            if name.lower() == "unknown": name = "unknown"
            PIF[pid] = name
    fsrch = ">Father<"
    msrch = ">Mother<"
    if ((fsrch in infoboxtxt) or (msrch in infoboxtxt)):
        # pull the data
        if (fsrch in infoboxtxt):
            loc = infoboxtxt.find(fsrch)
            ptx = tgcts(infoboxtxt[loc:], "td")
            pid = "nm_f"
            grabname(ptx, pid)
        if (msrch in infoboxtxt):
            loc = infoboxtxt.find(msrch)
            ptx = tgcts(infoboxtxt[loc:], "td")
            pid = "nm_m"
            grabname(ptx, pid)
    else:
        # if that doesn't work, try alternate formats
        srch = 'Parents'
        loc = infoboxtxt.find(srch)
        if loc == -1:
            srch = 'Relations'
            loc = infoboxtxt.find(srch)
        if loc == -1: return PIF
        parentdta = tgcts(infoboxtxt[loc:], "td")
        parents = alltgcts(parentdta, "li")
        for ptx in parents:
            if "mother" in ptx: pid = "nm_m"
            elif "father" in ptx: pid = "nm_f"
            else: continue
            grabname(ptx, pid)
    
    return PIF

def RecurPedigree(d=0, u="", Ped = {}):
    if DEPTH < d:
        print("recurse limit reached for", u)
        return None
    if u == 'unknown': return None
    if len(u) < 2: return None
    if u in Ped:
        # just use the cached data
        p = Ped[u]
    else:
        p = getwikiperson(u)
        if 'url' in p:
            u = p['url']
        Ped[u] = p
    if "nm_f" in p:
        RecurPedigree(d+1, p["nm_f"], Ped)
    if "nm_m" in p:
        RecurPedigree(d+1, p["nm_m"], Ped)

try:
    f = open(SAVEFILE, 'r')
    Total_Pedigree = eval(f.read())
    f.close()
except:
    Total_Pedigree = {}
RecurPedigree(0, ROOT_NAME, Total_Pedigree)
print(len(Total_Pedigree), "people recorded")
print("hand-check the following dead-ends")
for nm in Total_Pedigree:
    p = Total_Pedigree[nm]
    if 'url' not in p: continue
    if(('nm_f' not in p) and ('nm_f' not in p)):
        if (('b' in p) or ('d' in p)): p['nm_f'] = 'unknown'
        else: print(p['url'])
out = str(Total_Pedigree)
out = out.replace("}, ","},\n\n")
out = out.encode('ascii', 'ignore')
f = open(SAVEFILE, 'wb')
f.write(out)
f.close()

