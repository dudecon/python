# Ancestor_Compiler_WikiPedia.py Version 0.8
# Grabs ancestor data from WikiPedia
# The site to query
SITE = "https://en.wikipedia.org/wiki/"
# the page on the site to query
# ROOT_NAME = "John_Howard,_1st_Duke_of_Norfolk"
# ROOT_NAME = "Yaroslav_the_Wise"
ROOT_NAME = "Paul Daniel Spooner"
URL = SITE + ROOT_NAME
DEPTH = 67  # this should be plenty
# note that if you want to change either of these, you'll probably
# have to update the parsing code in the "except" below
PLAIN_NAME = ROOT_NAME.replace("_", " ")
CLEAN_NAME = PLAIN_NAME.replace(",", "")
SAVEFILE = F'Pedigree_{CLEAN_NAME}.txt'
# SAVEFILE = "Pedigree_John Howard 1st Duke of Norfolk.txt"
VERBOSE = True

INTERFACEHINT = "No or Unknown ancestor (and next), Obscure (and next)"
INTERFACEHINT += "\nSave (and exit)\nFather, Mother, Born, Died"

# Version History
# V 0.1 2021-11-29  Worked on it


from urllib.request import urlopen
import webbrowser


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
    substr = st[1 + stpos:edpos]
    return substr


def alltgcts(st, tg):
    # return a list of all the text enclosed by the specified tag
    strt = f"<{tg}"
    endt = f"</{tg}>"
    stpos = st.find(strt)
    allcontents = []
    while stpos != -1:
        edpos = st.find(endt, stpos)
        if edpos == -1: return allcontents
        stpos = st.find(">", stpos)
        substr = st[1 + stpos:edpos]
        allcontents.append(substr)
        stpos = st.find(strt, edpos)
    return allcontents


def cln(st):
    # clean out markup elements
    precull = ('\t',)
    excice = ('head', 'script', 'footer', 'sup', 'noscript', 'nav', 'form', 'cite', 'ol')
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


def getwikiperson(Url_Name):
    PIF = {'nm': Url_Name}
    # placeholder in case the site search fails for some reason
    try:
        with urlopen(SITE + Url_Name) as wkpg:
            html = wkpg.read()
    except:
        return PIF
    page = html.decode("utf-8")
    # populate the name field
    srch = 'id="firstHeading"'
    loc = page.find(srch)
    if loc == -1: return PIF
    tg = "h1"
    nametxt = tgcts(page[loc - 10:], tg)
    if len(nametxt) == 0: return PIF
    PIF['nm'] = nametxt
    # if we got this far, the URL is good, so let's save that
    PIF['url'] = Url_Name
    # find the infobox
    srch = 'class="infobox vcard"'
    loc = page.find(srch)
    if loc == -1:
        # no infobox! guess we don't have any dates or parents?
        return PIF
    tg = "table"
    infoboxtxt = tgcts(page[loc - 10:], tg)
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

    clnpage = cln(page).lower()
    if ('saint' in clnpage) and (
            ('canoni' in clnpage) or ('patron' in clnpage) or ('venerat' in clnpage)) and (
            'catholic' in clnpage):
        webbrowser.open(SITE + EntryUrl)
        check = input(f"If {nm} is a saint, what is their feast day? ")
        if check == 's': return PIF
        if len(check) > 4:
            p['s'] = check
        else:
            p['s'] = 'n'
    else:
        p['s'] = 'n'

    # find the parents
    # try Father and Mother first
    def grabname(proptxt, propid):
        # print(proptxt, propid)
        if ('href="' in proptxt) and ("redlink=1" not in proptxt):
            # get the href, so we can follow up on the ancestor
            lo = proptxt.find(srch)
            urlstart = proptxt.find('"', lo + 1) + 1 + 6
            urlend = proptxt.find('"', urlstart)
            newurl = proptxt[urlstart:urlend]
            PIF[propid] = newurl
        else:
            # no link, so strip it down and use it as the name
            name = tgx(proptxt, '(', ')')
            name = tgx(name, '<', '>')
            name = name.strip()
            if name.lower() == "unknown": name = "unknown"
            PIF[propid] = name

    fsrch = ">Father<"
    msrch = ">Mother<"
    if (fsrch in infoboxtxt) or (msrch in infoboxtxt):
        # pull the data
        if fsrch in infoboxtxt:
            loc = infoboxtxt.find(fsrch)
            ptx = tgcts(infoboxtxt[loc:], "td")
            pid = "nm_f"
            grabname(ptx, pid)
        if msrch in infoboxtxt:
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
            if "mother" in ptx:
                pid = "nm_m"
            elif "father" in ptx:
                pid = "nm_f"
            else:
                continue
            grabname(ptx, pid)

    return PIF


def dataentry(p):
    validkeys = ("f", "m", "b", "d", "yb", "yd", "nm")

    def processkey(k, desc, numeric=False):
        if k in p: print(p[k])
        intermediate = input(desc + ":")
        if intermediate == '': return  # no entry maintains existing data
        if numeric: intermediate = int(intermediate)
        p[k] = intermediate

    saveandexit = ''
    if p['nm'][-7:] == "bscure)":
        print("Obscure Figure")
        p['nm_f'] = 'unknown'
        if 'url' in p: del (p['url'])
        return 'n'
    print(p['nm'])
    while not saveandexit == 'y':
        choice = input(">:").lower()
        if choice == "n" or choice == "u":
            print("Unknown Parentage")
            p['nm_f'] = 'unknown'
            break
        elif choice == "o":
            print("Obscure Figure")
            p['nm'] = p['nm'] + " (obscure)"
            p['nm_f'] = 'unknown'
            if 'url' in p: del (p['url'])
            break
        elif choice == "s":
            print("Save and Exit")
            saveandexit = 'y'
        elif choice in validkeys:
            num = (choice in ('yb', 'yd'))
            processkey(choice, choice, num)
        elif (choice == "") or (choice == "?"):
            print(INTERFACEHINT)
        else:
            break
        if ('b' in p) and ('d' in p) and ('nm_f' in p) and ('nm_m' in p):
            # we've got all the data we could resonably expect
            break
    return saveandexit


def prinfo(p, gen):
    st = ''
    fst = ''
    nm = p['nm']
    if 's' in p:
        if p['s'] != 'n':
            if 'Saint ' not in nm: st = 'Saint '
            fst = " (" + p['s'] + ")"
    if gen == 0: return
    if p['g']:
        gt = 'Father'
    else:
        gt = 'Mother'
    ttl = ""
    if gen > 1: ttl = "Grand"
    if gen > 2: ttl = "Great-" + ttl
    if gen > 3: ttl = str(gen - 2) + ' ' + ttl
    if 'url' in p: url = '\n' + SITE + p['url']
    else: url = ''
    print(f"{st}{nm}{fst} is {ROOT_NAME}'s {ttl}{gt}{url}")


def DepthOfPedigree(u, Ped, d=0):
    totaldepth = d
    deepu = u
    if u == 'unknown': return 'u', 0
    if len(u) < 2: return 'n', 0
    if u not in Ped: return deepu, totaldepth
    p = Ped[u]
    for nmk in ("nm_m", "nm_f"):
        if nmk in p:
            otheru, otherdepth = DepthOfPedigree(p[nmk], Ped, d + 1)
            if otherdepth > totaldepth:
                deepu = otheru
                totaldepth = otherdepth
    return deepu, totaldepth


def OldestInPedigree(u, Ped):
    dtks = ('yb', 'yd')
    smallest_date = 9999
    if u not in Ped: return u, smallest_date
    p = Ped[u]
    deepest_u = ''  # I think this is okay, we will clobber it later
    for dtk in dtks:
        if dtk in p:
            if p[dtk] < smallest_date:
                smallest_date = p[dtk]
                deepest_u = u
    for ack in ("nm_m", "nm_f"):
        if ack in p:
            deeper_u, deeperdate = OldestInPedigree(p[ack], Ped)
            if deeperdate < smallest_date:
                smallest_date = deeperdate
                deepest_u = deeper_u
    return deepest_u, smallest_date


def FindInPedigree(u, Ped, name='', d=0, children=None, found=None):
    if children is None: children = set()
    if found is None: found = {}
    if DEPTH < d:
        if VERBOSE: print("recurse limit reached for", u)
        return None
    if u == 'unknown': return None
    if len(u) < 2: return None
    if u not in Ped: return None
    p = Ped[u]
    nm = p['nm']

    def recinfo():
        # record the entry info in the "found" log
        num_generations = len(children)
        if u not in found: found[u] = num_generations
        else: found[u] = min(num_generations, found[u])

    if len(name):
        # find the search string in the name
        if (name in nm) or (name in u):
            recinfo()
    else:
        # search for saints
        if 's' in p:
            if p['s'] != 'n':
                recinfo()

    newchildren = children.copy()
    newchildren.add(u)
    for k in ("nm_m", "nm_f"):
        if k in p: FindInPedigree(p[k], Ped, name, d + 1, newchildren, found)

    if d == 0:
        # we're back to the root level
        fdln = len(found)
        print(f'{fdln} records found')
        for u in found:
            gen = found[u]
            p = Ped[u]
            prinfo(p, gen)


def RecurPedigree(u="", Ped=None, d=0, children=None, curgender=1):
    if Ped is None: Ped = {}
    if children is None: children = set()
    if DEPTH < d:
        print("recurse limit reached for", u)
        return None
    if u == 'unknown': return None
    if len(u) < 2: return None
    if u in Ped:
        # just use the cached data
        p = Ped[u]
        # aggressive data entry query
        if ('nm_f' not in p) and ('nm_m' not in p):
            if 'url' in p:
                webbrowser.open(SITE + p['url'])
                dataentry(p)
    else:
        if ' ' in u:
            # it's not a wiki page address
            # it isn't cached
            p = {'nm': u}
            dataentry(p)
            Ped[u] = p
            # return None
        else:
            p = getwikiperson(u)
            Ped[u] = p
    if 'g' not in p:
        p['g'] = curgender
    if u in children:
        print("Causality loop detected for ", u)
        if VERBOSE: print(children)
        return None
    newchildren = children.copy()
    newchildren.add(u)
    for g, k in enumerate(("nm_m", "nm_f")):
        if k in p: RecurPedigree(p[k], Ped, d + 1, newchildren, curgender=g)


def gatherdata(tp):
    RecurPedigree(ROOT_NAME, tp, 0, set())
    print(len(tp), "people recorded")
    print("hand-check the following dead-ends")
    print(INTERFACEHINT)
    saveandexit = False
    while True:
        needdata = False
        for nm in tp:
            p = tp[nm]
            if ('nm_f' not in p) and ('nm_m' not in p):
                if 'url' in p:
                    webbrowser.open(SITE + p['url'])
                else:
                    continue
                needdata = True
                saveandexit = dataentry(p)
            if saveandexit == 'y': return True
        if needdata:
            RecurPedigree(ROOT_NAME, tp, 0, set())
        else:
            return False


def checksaints(tp):
    for nm in tp:
        p = tp[nm]
        if 'saint' in p: continue
        if 'url' not in p: continue
        EntryUrl = p['url']
        try:
            with urlopen(SITE + EntryUrl) as wkpg:
                html = wkpg.read()
        except:
            p['s'] = 'n'
            continue
        page = html.decode("utf-8")
        clnpage = cln(page).lower()
        if ('saint' in clnpage) and (
                ('canoni' in clnpage) or ('patron' in clnpage) or ('venerat' in clnpage)) and (
                'catholic' in clnpage):
            webbrowser.open(SITE + EntryUrl)
            check = input(f"If {nm} is a saint, what is their feast day? ")
            if check == 's': return
            if len(check) > 4:
                p['s'] = check
            else:
                p['s'] = 'n'
        else:
            p['s'] = 'n'


def cleandate(datea):
    datea = datea.strip()
    datea = tgx(datea, '(', ')')
    datea = datea.replace('&#8211;', '-')
    datea = datea.replace('&#8201;', ' ')
    datea = datea.replace('&#160;', ' ')
    if len(datea) < 3: return '', ''
    if not datea[-3:].isnumeric():
        e = len(datea)
        s = e - 3
        while s > 0:
            e -= 1
            s -= 1
            if datea[s:e].isnumeric(): break
            # found the last place there were three digits in a row
        if datea[s:e].isnumeric():
            pre = datea[e:].strip('.,;:?').strip() + ', '
            if len(pre) < 4: pre = ''
            newdatea = pre + datea[:e].strip('.,;:?').strip()
        ##            print(newdatea)
        ##            return newdatea
        else:
            newdatea = datea
    ##            print(datea)
    ##            newdatea = input(':')
    ##            return newdatea
    # now we have what we hope is a valid date at the end.
    # extract the number and do some more checks.
    else:
        newdatea = datea
    e = len(newdatea)
    s = e - 3
    while s > 0:
        s -= 1
        if not newdatea[s:e].isnumeric():
            s += 1
            break
    try:
        year = int(newdatea[s:e])
    except:
        year = 9999
    if year > 1990:
        print((newdatea, year))
        revised_datea = input('new data:')
        if revised_datea == '':
            return newdatea, ''
        newdatea = revised_datea
        year = input('new year:')
        if year != '':
            try:
                year = int(year)
            except:
                year = ''
    return newdatea, year


def finddatesinname(p):
    searchstrings = {'died': 'yd', 'born': 'yb'}
    searchinfo = [p['nm']]
    if 'url' in p: searchinfo.append(p['url'])
    for s in searchinfo:
        for ss in searchstrings:
            if ss in s:
                if searchstrings[ss] in p:
                    print(p[searchstrings[ss]], s)
                    continue
                else:
                    print(s)
                return dataentry(p)
    return False


def reprocess(tp):
    AllNames = {}
    for u in tp:
        p = tp[u]
        nm = p['nm']
        if nm in AllNames:
            AllNames[nm].append(u)
        else:
            AllNames[nm] = [u, ]
        # continue
        if finddatesinname(p): return True
        # continue
        if ('b' in p) and ('yb' not in p):
            p['b'], p['yb'] = cleandate(p['b'])
            if len(p['b']) < 3: del (p['b'])
            if p['yb'] == '': del (p['yb'])
        if ('d' in p) and ('yd' not in p):
            p['d'], p['yd'] = cleandate(p['d'])
            if len(p['d']) < 3: del (p['d'])
            if p['yd'] == '': del (p['yd'])

    for nm in AllNames:
        us = AllNames[nm]
        if len(us) > 1:
            print(us)
            for u in us: print(tp[u])
            print('\n')


def randcestor(tp):
    allurls = []
    for u in tp:
        p = tp[u]
        if 'url' in p: allurls.append(p['url'])
    from random import choice
    numchoices = len(allurls)
    chosenurl = choice(allurls)
    print(f'{chosenurl} selected from {numchoices} options')
    webbrowser.open(SITE + chosenurl)
    FindInPedigree(ROOT_NAME, tp, chosenurl)


def aveGeneration(TP):
    dtk = 'yb'
    entriesbygender = [0, 0, 0, 0]
    sumbygender = [0, 0, 0, 0]
    for nm in TP:
        p = TP[nm]
        if dtk not in p: continue  # no year born means no point!
        year_born = p[dtk]
        selfg = p['g']
        if 'yd' in p:
            age = p['yd'] - year_born
            entriesbygender[2+selfg] += 1
            sumbygender[2+selfg] += age
        for g, k in enumerate(("nm_m", "nm_f")):
            if k in p:
                ancnm = p[k]
                if ancnm in TP:
                    anc = TP[ancnm]
                    if dtk in anc:
                        entriesbygender[g] += 1
                        sumbygender[g] += year_born - anc[dtk]
    aveagebygender = []
    # print(entriesbygender)
    for i, v in enumerate(sumbygender):
        aveagebygender.append(v / entriesbygender[i])
    return aveagebygender


Total_Pedigree = {}


def loadfile():
    global Total_Pedigree
    try:
        f = open(SAVEFILE, 'r')
        alldata = f.read()
        f.close()
        Total_Pedigree = eval(alldata)
        if VERBOSE: print('file loaded')
    except:
        if VERBOSE: print('exception found')
        Total_Pedigree = {}
    if VERBOSE:
        lnpd = len(Total_Pedigree)
        print(f'{lnpd} entries in pedigree')


def savefile():
    out = str(Total_Pedigree)
    out = out.replace("}, ", "},\n\n")
    out = out.encode('ascii', 'ignore')
    f = open(SAVEFILE, 'wb')
    f.write(out)
    f.close()


loadfile()

INPUTLOOPHELP = 'Find, Info, Save, Load, eXit, Reprocess, Gather data, rAndom wiki page\n'
keep_at_it = True
while keep_at_it:
    c = input(">:").lower()
    if c == 's':
        savefile()
    elif c == 'l':
        loadfile()
    elif c == 'x':
        break
    elif c == 'f':
        srchstr = input('Search for:')
        if srchstr == 'saint': srchstr = ''
        FindInPedigree(ROOT_NAME, Total_Pedigree, srchstr)
    elif c == 'i':
        lnpd = len(Total_Pedigree)
        print(f'{lnpd} entries in pedigree')
        dpnm, dppd = DepthOfPedigree(ROOT_NAME, Total_Pedigree)
        print(f'deepest ancestor {dpnm} is {dppd} generations deep')
        oldest_nm, oldest_dt = OldestInPedigree(ROOT_NAME, Total_Pedigree)
        print(f'the oldest date is {oldest_dt} for {oldest_nm}')
        mage, fage, agew, agem = aveGeneration(Total_Pedigree)
        print(f'average generational spacing is\n{fage:.3} years for fathers\n{mage:.3} years for mothers')
        print(f'average lifespan is {agew:.3}W and {agem:.3}M')
    elif c == 'r': reprocess(Total_Pedigree)
    elif c == 'g': gatherdata(Total_Pedigree)
    elif c == 'a': randcestor(Total_Pedigree)
    else: print(INPUTLOOPHELP)
