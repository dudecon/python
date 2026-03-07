# Ancestor_Compiler_WikiPedia.py Version 0.8
# Grabs ancestor data from WikiPedia
# The site to query
SITE = "https://en.wikipedia.org/wiki/"
# the page on the site to query
# ROOT_NAME = "John_Howard,_1st_Duke_of_Norfolk"
# ROOT_NAME = "Yaroslav_the_Wise"
# ROOT_NAME = "Vladimir_the_Great"
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
UseWebBrowser = True

INTERFACEHINT = "No or Unknown ancestor (and next), Obscure (and next)"
INTERFACEHINT += "\nSave (and exit)\nFather, Mother, Born, Died"

# Version History
# V 0.1 2021-11-29  Worked on it
# V 0.2 2026-03-06  More Progress

if VERBOSE: print(SAVEFILE)


from urllib.request import urlopen
import webbrowser
from time import sleep
from random import choice

import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
os.chdir(SCRIPT_DIR)


def tgx(st, strt, endt):
    """Remove all substrings between strt and endt (inclusive) repeatedly."""
    while True:
        stpos = st.find(strt)
        if stpos == -1: break
        edpos = st.find(endt, stpos)
        if edpos == -1: break
        edpos += len(endt)
        st = st[:stpos] + st[edpos:]
    return st


def tgcts(st, tg):
    """Extract text content between the first <tg> and </tg> tags."""
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
    """Return list of all text contents enclosed by <tg>...</tg> tags."""
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
    """Strip HTML-like tags, scripts, styles, and normalize whitespace."""
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


def extract_dates(p):
    """Convert raw birth/death strings → cleaned string + year (if possible)."""
    for dk in ('b', 'd'):
        yk = 'y'+dk
        if (dk in p) and (yk not in p):
            p[dk], p[yk] = cleandate(dk,p)
            if len(p[dk]) < 3: del (p[dk])
            if p[yk] == '': del (p[yk])


def getwikiperson(Url_Name):
    """
    Fetch and parse Wikipedia page for a person.
    Returns dict with name, url, birth, death, father, mother, saint info (if applicable).
    """
    PIF = {'nm': Url_Name}
    # placeholder in case the site search fails for some reason
    try:
        with urlopen(SITE + Url_Name) as wkpg:
            html = wkpg.read()
            sleep(choice((1.618,1,0.618)))
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

    extract_dates(PIF)

    clnpage = cln(page).lower()
    if ('saint' in clnpage) and (
            ('canoni' in clnpage) or ('patron' in clnpage) or ('venerat' in clnpage)) and (
            'catholic' in clnpage):
        if UseWebBrowser: webbrowser.open(SITE + Url_Name)
        nm = PIF['nm']
        check = input(f"If {nm} is a saint, what is their feast day? ")
        if check == 's': return PIF
        if len(check) > 4:
            PIF['s'] = check
        else:
            PIF['s'] = 'n'
    else:
        PIF['s'] = 'n'

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
            pid = 'f'
            grabname(ptx, pid)
        if msrch in infoboxtxt:
            loc = infoboxtxt.find(msrch)
            ptx = tgcts(infoboxtxt[loc:], "td")
            pid = 'm'
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
                pid = 'm'
            elif "father" in ptx:
                pid = 'f'
            else:
                continue
            grabname(ptx, pid)

    return PIF


def dataentry(p, autoexit = True):
    """
    Interactive prompt to fill in missing parent / date information for a person.
    Returns 'y' if user chooses to save and exit, otherwise None/'n'.
    """
    validkeys = ("f", "m", "b", "d", "yb", "yd", "nm")

    def processkey(k, desc, numeric=False):
        current = p.get(k, "(not set)")
        print(f"Current {desc}: {current}")
        while True:
            val = input(f"{desc}: ").strip()
            
            if not val:
                return  # keep existing / no change

            if val in ("ERASE",'-'):
                if k == 'nm':
                    print("Nice try, but you can't erase someone's name")
                    continue
                elif input("Are you sure? type 'Y' (case sensitive)") == "Y":
                    del p[k]
                    print(f"Key {k} removed")
                    break

            if numeric:
                if val.lstrip('-').isdigit():
                    p[k] = int(val)
                    break
                else:
                    print("Please enter a valid integer year (e.g. 1453, -300).")
                    continue

            # Name / URL fields – minimal validation
            elif len(val) == 1 and val.lower() not in ('?'):
                print("Name too short — enter at least 2 characters, '?', or leave blank.")
                continue
            elif k in ('f', 'm', 'nm') and ('http' in val.lower() or 'wiki' in val.lower()):
                print("For name or parents enter the plain name or wiki page title only (not full URL).")
                continue

            p[k] = val
            break

    saveandexit = ''
    if 0:# ('f' not in p) and ('m' not in p):
        print("unknown parentage")
        p['f'] = 'unknown'
        return 'n'
    if 0:# len(p['nm'].split()) < 2:
        p['nm'] = p['nm'] + " (obscure)"

    
    if p.get('nm', '').endswith('bscure)'):
        print("Obscure Figure")
        p['f'] = 'unknown'
        if 'url' in p: del (p['url'])
        return 'n'

    
    for k in validkeys:
        if k in p: print(k, "is", p[k])
    while saveandexit != 'y':
        extract_dates(p)
        choice = input("edit >:").lower()
        if choice == "n" or choice == "u":
            print("Unknown Parentage")
            p['f'] = 'unknown'
            break
        elif choice == "o":
            print("Obscure Figure")
            p['nm'] = p['nm'] + " (obscure)"
            p['f'] = 'unknown'
            if 'url' in p: del (p['url'])
            break
        elif choice == "s":
            print("Save and Exit")
            saveandexit = 'y'
        elif choice == "q":
            print("Exit without saving to disk")
            saveandexit = 'n'
            break
            
        elif choice in validkeys:
            numeric = choice in ('yb', 'yd')
            desc_map = {
                'f':  'Father (wiki title or name)',
                'm':  'Mother (wiki title or name)',
                'b':  'Birth (full text)',
                'd':  'Death (full text)',
                'yb': 'Birth year',
                'yd': 'Death year',
                'nm': 'Name'
            }
            processkey(choice, desc_map.get(choice, choice), numeric=numeric)
            
        elif choice in ('', '?', 'h', 'help'):
            print(INTERFACEHINT)
            print("  q     = quit without saving")
            for k in validkeys:
                if k in p: print(k, "is", p[k])
        else:
            print("unknown command, '?', 'h', 'help' for help.")
        if autoexit and all(k in p for k in ('b', 'd', 'f', 'm')):
            # we've got all the data we could resonably expect
            break
    return saveandexit


def prinfo(p, gen):
    """Print formatted ancestor relationship line (with optional browser open)."""
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
    if 'url' in p:
        url = '\n' + SITE + p['url']
        if UseWebBrowser: webbrowser.open(SITE + p['url'])
    else: url = ''
    print(f"{st}{nm}{fst} is {ROOT_NAME}'s {ttl}{gt}{url}")


def DepthOfPedigree(u, Ped, d=0):
    """Return deepest known ancestor name and its generation depth."""
    totaldepth = d
    deepu = u
    if u == 'unknown': return 'u', 0
    if len(u) < 2: return 'n', 0
    if u not in Ped: return deepu, totaldepth
    p = Ped[u]
    for nmk in ('m', 'f'):
        if nmk in p:
            otheru, otherdepth = DepthOfPedigree(p[nmk], Ped, d + 1)
            if otherdepth > totaldepth:
                deepu = otheru
                totaldepth = otherdepth
    return deepu, totaldepth


def OldestInPedigree(u, Ped):
    """Return person with earliest known birth/death year and that year."""
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
    for ack in ('m', 'f'):
        if ack in p:
            deeper_u, deeperdate = OldestInPedigree(p[ack], Ped)
            if deeperdate < smallest_date:
                smallest_date = deeperdate
                deepest_u = deeper_u
    return deepest_u, smallest_date


def FindInPedigree(u, Ped, name='', d=0, children=None, found=None):
    """
    Search pedigree for matching names or saints and print relationship paths.
    When name='', searches for anyone marked as a saint.
    """
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
    for k in ('m', 'f'):
        if k in p: FindInPedigree(p[k], Ped, name, d + 1, newchildren, found)

    if d == 0:
        # we're back to the root level
        fdln = len(found)
        print(f'{fdln} records found')
        global UseWebBrowser
        if fdln > 3 and UseWebBrowser:
            print('turning off wiki page opening')
            UseWebBrowser = False
        for u in found:
            gen = found[u]
            p = Ped[u]
            prinfo(p, gen)


def RecurPedigree(u="", Ped=None, d=0, children=None, curgender=1):
    """
    Recursively build/extend pedigree starting from u.
    Returns 's' if user saved & exited during data entry.
    """
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
        if ('f' not in p) and ('m' not in p):
            if 'url' in p:
                if UseWebBrowser: webbrowser.open(SITE + p['url'])
                if dataentry(p) == 'y': return 's'
    else:
        if ' ' in u:
            # it's not a wiki page address
            # it isn't cached
            p = {'nm': u}
            if dataentry(p) == 'y': return 's'
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
    for g, k in enumerate(('m', 'f')):
        if k in p:
            if RecurPedigree(p[k], Ped, d + 1, newchildren, curgender=g) == 's':
                return 's'


def gatherdata(tp):
    """
    Main data collection loop: recurse + interactively fill missing parents.
    Returns True if user chose to save & exit during any phase.
    """
    if RecurPedigree(ROOT_NAME, tp, 0, set()) == 's':
        return True

    print(f"\n{len(tp)} people recorded")
    showhelp = True

    while True:
        # Phase 1: automatic dead-end filling
        dead_ends = []
        for nm in sorted(tp):
            p = tp[nm]
            if ('f' not in p) and ('m' not in p):
                if p.get('nm', '').endswith('bscure)'):
                    continue
                dead_ends.append((nm, p))

        if dead_ends:
            print("\nHand-check the following dead-ends:")
            print(INTERFACEHINT)
            needdata = False
            for nm, p in dead_ends:
                print(f"\nEntry: {nm}")
                if 'url' in p:
                    if UseWebBrowser:
                        webbrowser.open(SITE + p['url'])
                saveandexit = dataentry(p)
                if saveandexit == 'y':
                    return True
                needdata = True

            # After processing current dead-ends → try to recurse again
            if needdata:
                if RecurPedigree(ROOT_NAME, tp, 0, set()) == 's':
                    return True
            continue  # loop back to find new dead-ends

        # Phase 2: no more dead-ends → offer manual editing
        if showhelp:
            print("\nNo more automatic dead-ends found.")
            print("Manual editing mode. Available commands:")
            print("  e / edit <name or substring>   → find and edit matching entries")
            print("  list                       → show all entries (numbered)")
            print("  show <number or name>      → display one entry")
            print("  s / save                   → save changes to disk and exit gatherdata")
            print("  x / q / exit               → quit editing (changes remain in memory)")
            print("  r / l / reload                 → reload from disk (discard in-memory changes)")
            print("  ? / help                   → show this help")
            showhelp = False

        cmd = input("\ngather >: ").strip().lower()

        if cmd in ('x', 'exit', 'q'):
            return False

        elif cmd in ('s', 'save'):
            return True
        
        elif cmd in ('r', 'l', 'reload'):
            print("Reloading pedigree from disk — unsaved changes will be lost.")
            loadfile()
            tp = Total_Pedigree
            continue

        elif cmd == '?' or cmd == 'help':
            showhelp = True
            continue

        elif cmd == 'list':
            print("\nAll entries:")
            for i, nm in enumerate(sorted(tp), 1):
                p = tp[nm]
                parents = ""
                if 'f' in p or 'm' in p:
                    parents = f"  (f:{p.get('f','?')}, m:{p.get('m','?')})"
                print(f"{i:4d}. {nm}{parents}")
            continue

        elif cmd.startswith('show '):
            arg = cmd[5:].strip()
            found = []
            try:
                idx = int(arg) - 1
                names = sorted(tp)
                if 0 <= idx < len(names):
                    found = [names[idx]]
            except ValueError:
                # name/substring search
                arg_lower = arg.lower()
                found = [nm for nm in tp if arg_lower in nm.lower()]

            if not found:
                print("No matching entry.")
                continue

            for nm in found:
                print(f"\n--- {nm} ---")
                p = tp[nm]
                for k in sorted(p):
                    print(f"  {k:3}: {p[k]}")
            continue

        elif cmd.startswith('edit ') or cmd.startswith('e '):
            arg = ' '.join(cmd.split(" ")[1:])
            if not arg:
                print("Usage: edit <name or substring>")
                continue

            matches = [nm for nm in tp if arg.lower() in nm.lower()]
            if not matches:
                print("No matching entries found.")
                continue

            if len(matches) > 1:
                print(f"Multiple matches ({len(matches)}):")
                for i, nm in enumerate(matches, 1):
                    print(f"  {i}. {nm}")
                try:
                    sel = int(input("Select number to edit (or Enter to cancel): "))
                    if not (1 <= sel <= len(matches)):
                        continue
                    to_edit = matches[sel-1]
                except:
                    continue
            else:
                to_edit = matches[0]
                print(f"Editing: {to_edit}")

            if UseWebBrowser and 'url' in tp[to_edit]:
                webbrowser.open(SITE + tp[to_edit]['url'])

            if dataentry(tp[to_edit],False) == 'y':
                return True

            continue

        else:
            print("Unknown command. Type ? for help.")


def checksaints(tp):
    """Check Wikipedia pages for saint status and ask user for feast day if found."""
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
            if UseWebBrowser: webbrowser.open(SITE + EntryUrl)
            check = input(f"If {nm} is a saint, what is their feast day? ")
            if check == 's': return
            if len(check) > 4:
                p['s'] = check
            else:
                p['s'] = 'n'
        else:
            p['s'] = 'n'


def cleandate(key,person):
    """Clean date string and attempt to extract 4-digit year."""
    datea = person[key]
    datea = datea.strip()
    datea = tgx(datea, '(', ')')
    datea = datea.replace('&#8211;', '-')
    datea = datea.replace('&#8201;', ' ')
    datea = datea.replace('&#160;', ' ').strip()
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
        else:
            newdatea = datea
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
        year = 999999
    if year > 1990 or year < 500:
        print("person named", person['nm'], "data for", key)
        if year == 999999: print(f"no date found in {datea!r}")
        elif year > 1990: print(f"Modern-looking date detected: {datea!r} → year {year}")
        elif year < 500: print(f"Very old-looking date detected: {datea!r} → year {year}")
        revised = input("Corrected date string (Enter to keep): ").strip()
        if revised:
            datea = revised
            yr_input = input("Corrected year (Enter to keep): ").strip()
            if yr_input.isdigit():
                year = int(yr_input)
            
            elif yr_input:
                year = ''   # clear if nonsense
        elif year == 999999:
            year = ''   # failure to parse, no entry
        # No else: keep original year if user just presses Enter

    datea = datea.strip(' ,.;:-')

    return datea, year


def finddatesinname(p):
    """Look for 'born'/'died' in name or URL and prompt for dates if found."""
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
    """Extract dates, fix name→parent confusion, report duplicate names."""
    AllNames = {}
    for u in tp:
        p = tp[u]
        nm = p['nm']
        if nm in AllNames:
            AllNames[nm].append(u)
        else:
            AllNames[nm] = [u, ]
        # continue
        extract_dates(p)
        # continue
        if finddatesinname(p): return True
        # continue
        for gk in ('f', 'm'):
            ogk = 'nm_'+gk
            if ogk in p:
                p[gk] = p[ogk]
                del(p[ogk])
        

    for nm in AllNames:
        us = AllNames[nm]
        if len(us) > 1:
            print(us)
            for u in us: print(tp[u])
            print('\n')


def randcestor(tp):
    """Open random ancestor Wikipedia page and show their relationship to the root."""
    allurls = []
    for u in tp:
        p = tp[u]
        if 'url' in p: allurls.append(p['url'])
    from random import choice
    numchoices = len(allurls)
    chosenurl = choice(allurls)
    print(f'{chosenurl} selected from {numchoices} options')
    FindInPedigree(ROOT_NAME, tp, chosenurl)


def aveGeneration(TP):
    """
    Calculate average father/mother age at child's birth and average lifespan.
    Returns tuple: (mother avg age at birth, father avg age at birth,
                    women avg lifespan, men avg lifespan)
    """
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
        for g, k in enumerate(('m', 'f')):
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

import ast

def loadfile():
    """Load pedigree dictionary from SAVEFILE (eval-based NOT SECURE)."""
    global Total_Pedigree
    try:
        with open(SAVEFILE, encoding='utf-8') as f:
            alldata = f.read()
        Total_Pedigree = ast.literal_eval(alldata)
        if VERBOSE:
            print('file loaded')
    except Exception as e:
        if VERBOSE:
            print(f'Load failed: {e.__class__.__name__}: {e}')
        Total_Pedigree = {}
    if VERBOSE:
        print(f'{len(Total_Pedigree)} entries in pedigree')


def savefile():
    """Save pedigree dictionary to SAVEFILE in readable-ish format."""
    out = str(Total_Pedigree)
    out = out.replace("}, ", "},\n\n")
    out = out.encode('ascii', 'ignore')
    f = open(SAVEFILE, 'wb')
    f.write(out)
    f.close()


loadfile()

INPUTLOOPHELP = 'Find, Info, Save, Load, eXit, Reprocess, Gather data, rAndom wiki page, open Web page\n'
keep_at_it = True
while keep_at_it:
    c = input("main >:").lower()
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
        print(f'average lifespan is {agew:.3} for women and {agem:.3} for men')
    elif c == 'r': reprocess(Total_Pedigree)
    elif c == 'g':
        if gatherdata(Total_Pedigree): savefile()
    elif c == 'a': randcestor(Total_Pedigree)
    elif c == 'w':
        UseWebBrowser = not UseWebBrowser
        print(f'open wiki pages set to {UseWebBrowser}')
    else: print(INPUTLOOPHELP)
