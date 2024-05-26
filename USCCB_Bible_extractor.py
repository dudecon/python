#USCCB Bible Downloader
#for personal use only

SITE = "https://bible.usccb.org/bible/"
DEBUG = False

from urllib.request import urlopen
import webbrowser
from HTML_Cleaner import *


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
