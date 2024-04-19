#USCCB Bible Downloader
#for personal use only

SITE = "https://bible.usccb.org/bible/"
DEBUG = False

from urllib.request import urlopen
import webbrowser

#++++++++++++++++ HTML helper functions +++++++++++++++++

def find_tag_bounds(html, tag):
    # use for nested tags
    # to remove the tags themselves, use tgx()
    tag_label = tag.split()[0]
    start_tag = f"<{tag}"  # Specific tag with attributes at depth 0
    all_start = f"<{tag_label}"  # Any tag of this type for nested checks
    end_tag = f"</{tag_label}>"
    # if DEBUG: print("finding", tag)

    bounds = []
    depth = 0
    pos = 0
    thisbound = []
    while True:
        if depth == 0 and len(thisbound) == 0:
            start_pos = html.find(start_tag, pos)  # Look for specific tag at base depth
            if start_pos == -1:
                break
            thisbound.append(start_pos)
            end_search_start = html.find('>', start_pos) + 1
            pos = end_search_start
            start_pos = html.find(all_start, pos)
        else:
            start_pos = html.find(all_start, pos)  # Look for any tag of this type when nested
            end_search_start = pos # and search for the end tag from the same point

        # if DEBUG: print("depth",depth,"start",start_pos)

        
        end_pos = html.find(end_tag, end_search_start)
        # if DEBUG: print("depth",depth,"end",end_pos)

        if end_pos == -1:
            # close out the current bounds with the end of file and return everything
            thisbound.append(len(html)-1)
            bounds.append(thisbound)
            return bounds

        if (start_pos < end_pos) and not (start_pos == -1):
            # found another start, before the next end tag
            pos = html.find('>', start_pos) + 1
            depth += 1
            continue
        else:
            # found an end tag before the next start tag
            if depth == 0:
                thisbound.append(end_pos)
                bounds.append(thisbound)
                thisbound = []
            else:
                depth -= 1
            pos = end_pos + len(end_tag)
            continue

    
    return bounds


def extract_contents(html, tag):
    bounds = find_tag_bounds(html, tag)
    if DEBUG: print("bounds",bounds)
    if len(bounds):
        contents = [html[html.find('>', start) + 1:end].strip() for start, end in bounds]
        return contents
    else:
        return []  # Return an empty list if no bounds were found
    

def excise_content(html, tag):
    tag_label = tag.split()[0]
    end_tag = f"</{tag_label}>"
    bounds = find_tag_bounds(html, tag)
    # Process bounds from last to first to avoid messing up the indices
    for start, end in reversed(bounds):
        html = html[:start] + html[end+len(end_tag):]
    return html


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


def cln(st):
    # clean out markup elements
    precull = ('\t',)
    excice = ('head', 'script', 'footer', 'sup', 'noscript', 'nav', 'form', 'cite', 'ol', 'style data',
              'span class="bcv"')
    detag = ('html', 'div', 'body', '!DOCTYPE', 'a', '!--', 'img', 'style',
             'li', 'td', 'ul', 'tr', 'tbody', 'table', 'h1', 'h2', 'h3', 'h4',
             'span', 'th', 'p', 'i', 'b', 'small', 'label', 'dd', 'dl', 'dt', 'blockquote',
             'center',)
    postcull = ('</abbr>', '[edit]')
    replacement = (('&lt;', '<'), ('&gt;', '>'), ('&amp;', '&'),
                   ('&euro;', '€'), ('&pound;', '£'), ('&quot;', '"'), ('&apos;', "'"),
                   ('&nbsp;', ' '), ('&ensp;', ' '), ('&emsp;', ' '), ('&emsp13;', ' '),
                   ('&numsp;', ' '), ('&puncsp;', ' '), ('&thinsp;', ' '), ('&hairsp;', ' '),
                   ('  ', ' '), (' \n', '\n'), ('\n\n', '\n'),
                   )
    for tg in precull:
        if DEBUG: print(len(st))
        if DEBUG: print(tg)
        st = st.replace(tg, '')
    for tg in excice:
        st = excise_content(st, tg)
    for tg in detag:
        st = tgx(st, f'<{tg}', '>')
        st = st.replace(f'</{tg}>', '')
    for tg in postcull:
        st = st.replace(tg, '')
    for (rpl1, rpl2) in replacement:
        while rpl1 in st:
            st = st.replace(rpl1, rpl2)
    return st

#++++++++++++++++ Bible extraction functions ++++++++++++++++

def get_bible_book(book_name="preface",chapter_number = "0"):
    try:
        with urlopen(SITE + book_name + '/' + chapter_number) as wkpg:
            html = wkpg.read()
    except:
        return None
    page = html.decode("utf-8")
    return page



h = get_bible_book("genesis","3")
print("raw html ", len(h), "chars")
c = extract_contents(h, 'div class="content"')[0]
print("page content", len(c), "chars")
t = extract_contents(c, 'li class="pager__item is-active"')
if len(t) > 1:
    if t[0] != t[1]: print('mismatched title',t)
txt = cln(extract_contents(c, 'div class="contentarea"')[0])
print("\ntitle:\n")
print(t[0])
print("\ntext:\n")
print(txt)
