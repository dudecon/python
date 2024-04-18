#USCCB Bible Downloader
#for personal use only

SITE = "https://bible.usccb.org/bible/"
DEBUG = True

from urllib.request import urlopen
import webbrowser

#++++++++++++++++ HTML helper functions +++++++++++++++++


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

def all_tag_contents(html, tag):
    # return all the text enclosed by the specified tag
    # can handle nesting, but only finds the first occurance
    # Prepare the start and end markers for the tag
    start_tag = f"<{tag}"
    tag_label = tag.split()[0]
    all_start = f"<{tag_label}"
    end_tag = f"</{tag_label}>"
    
    # Find all positions of the tag's start and end
    stack = []
    tag_contents = []
    pos = 0

    start_pos = html.find(start_tag, pos)
    
    while True:
        # Find the next end tag occurrence
        end_pos = html.find(end_tag, pos)
        
        # If no more tags are found, break the loop
        if start_pos == -1 and end_pos == -1:
            break
        
        # If a start tag is found and either there is no end tag or start tag is before the end tag
        if start_pos != -1 and (start_pos < end_pos or end_pos == -1):
            # Move the position just past the '>'
            pos = html.find('>', start_pos)
            stack.append(pos + 1)
            pos += 1  # Move past '>'
        elif end_pos != -1 and (end_pos < start_pos or start_pos == -1):
            # An end tag is found and either there is no start tag or end tag is before the start tag
            if stack:
                start = stack.pop()
                if not stack:  # Only consider non-nested or properly closed tags
                    tag_contents.append(html[start:end_pos])
            pos = end_pos + len(end_tag)
        # Find the next start tag occurrence
        if stack:
            start_pos = html.find(all_start, pos)
        else:
            start_pos = html.find(start_tag, pos)
    
    return tag_contents

def find_tag_bounds(html, tag, start=0, depth=0):
    tag_label = tag.split()[0]
    start_tag = f"<{tag}"  # Specific tag with attributes at depth 0
    all_start = f"<{tag_label}"  # Any tag of this type for nested checks
    end_tag = f"</{tag_label}>"
    found_start = 0
    found_end = -1
    # if DEBUG: print("finding", tag)

    pos = start
    while True:
        if depth == 0:
            start_pos = html.find(start_tag, pos)  # Look for specific tag at base depth
        else:
            start_pos = html.find(all_start, pos)  # Look for any tag of this type when nested

        # if DEBUG: print("depth",depth,"start",start_pos)
        if start_pos != -1:
            # Move past the '>' of the start tag to begin content capture
            next_search_start = html.find('>', start_pos) + 1
        else:
            next_search_start = pos
        
        end_pos = html.find(end_tag, next_search_start)
        # if DEBUG: print("depth",depth,"end",end_pos)

        if end_pos == -1:
            return bounds, None

        if start_pos == -1:
            break

        if start_pos < end_pos:
            # found another start, before the next end tag
            pos = html.find('>', start_pos) + 1
            inner_bounds, pos = find_tag_bounds(html, tag_label, pos, depth+1)
            if ((depth == 0 or pos is None) and inner_bounds):
                # Collect entire segment from the original start to the final end in this scope
                bounds.append((inner_bounds[0][0], inner_bounds[-1][1]))
        else:
            return bounds, end_pos + len(end_tag)

        if depth == 0 and start_pos != -1:
            pos = end_pos + len(end_tag)
    
    if depth == 0:
        return bounds
    else:
        return bounds, pos

def extract_contents(html, tag):
    bounds = find_tag_bounds(html, tag)
    if DEBUG: print("bounds",bounds)
    if len(bounds):
        contents = [html[start:end].strip() for start, end in bounds]
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
        print(len(st))
        print(tg)
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

#++++++++++++++++ Bible extraction functions ++++++++++++++++

def get_bible_book(book_name="preface",chapter_number = "0"):
    try:
        with urlopen(SITE + book_name + '/' + chapter_number) as wkpg:
            html = wkpg.read()
    except:
        return None
    page = html.decode("utf-8")
    return page



h = get_bible_book("genesis")
print("raw html ", len(h), "chars")
c = extract_contents(h, 'div class="content"')[0]
print("page content", len(c), "chars")
t = extract_contents(c, 'li class="pager__item is-active"')
if t[0] != t[1]: print('mismatched title',t)
txt = cln(extract_contents(c, 'div class="contentarea"')[0])
print(t[0])
print(txt)
