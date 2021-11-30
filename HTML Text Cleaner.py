# HTML Text Cleaner.py Version 0.1
# The file to edit
FILEPATH = "Survey Relationship.txt"
NEWFILESUFFIX = 'cleaned'

# Version History
# V 0.1 2021-11-29  Worked on it

try:
    f = open(FILEPATH, 'r')
    raw = f.read()
    f.close()
except:  # File not found or whatever
    print('file load error')
    raw = ''


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
    excice = ('head', 'script', 'footer', 'sup', 'noscript', 'nav', 'form', 'cite', 'ol')
    detag = ('html', 'div', 'body', '!DOCTYPE', 'a', '!--', 'img', 'style',
             'li', 'td', 'ul', 'tr', 'tbody', 'table', 'h1', 'h2', 'h3', 'h4',
             'span', 'th', 'p', 'i', 'b', 'small', 'label', 'dd', 'dl', 'dt', 'blockquote',
             'textarea')
    postcull = ('</abbr>', '[edit]')
    replacement = (('\n\n','\n'), ('&lt;','<'), ('&gt;','>'), ('&amp;','&'), 
    ('&euro;','€'), ('&pound;','£'), ('&quot;','"'), ('&apos;',"'"), 
    ('&nbsp;',' '), ('&ensp;',' '), ('&emsp;',' '), ('&emsp13;',' '), 
    ('&numsp;',' '), ('&puncsp;',' '), ('&thinsp;',' '), ('&hairsp;',' '), 
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

debugfind = '#progress-bar'
if debugfind in raw:
    pos = raw.find(debugfind)
    STRT = max(pos-400,0)
    END = min(pos+400,len(raw)-1)
    print('---FOUND TEXT---\n', raw[STRT:END] )

print('---RAW TEXT---\n', raw[:200], '\n[......]\n', raw[-200:], )
cleaned = cln(raw)
print('---CLEANED TEXT---\n', cleaned[:200], '\n[......]\n', cleaned[-200:], )

if len(cleaned) == 0: print('There was nothing left after cleaning.\nIt was all cleaned away!')
else:
    splitfile = FILEPATH.split('.')
    splitfile.append(splitfile[-1])
    splitfile[-2] = NEWFILESUFFIX
    savefile = '.'.join(splitfile)

    try:
        f = open(savefile, 'w')
        f.write(cleaned)
        f.close()
    except:  # File not found or whatever
        print("file save error, here's the cleaned text")
        print(cleaned)