#USCCB Bible Downloader
#for personal use only

SITE = "https://bible.usccb.org/bible/"
DEBUG = False

from urllib.request import urlopen
import webbrowser
from HTML_Cleaner import *
from time import sleep
from random import choice

allbooks = (("preface",0),
            ("genesis",50),
            ("exodus",40),
            ("leviticus",27),
            ("numbers",36),
            ("deuteronomy",34),
            ("joshua",24),
            ("judges",21),
            ("ruth",4),
            ("1samuel",31),
            ("2samuel",24),
            ("1kings",22),
            ("2kings",25),
            ("1chronicles",29),
            ("2chronicles",36),
            ("ezra",10),
            ("nehemiah",13),
            ("tobit",14),
            ("judith",16),
            ("esther",10),
            ("1maccabees",16),
            ("2maccabees",15),
            ("job",42),
            ("psalms",150),
            ("proverbs",31),
            ("ecclesiastes",12),
            ("songofsongs",8),
            ("wisdom",19),
            ("sirach",51),
            ("isaiah",66),
            ("jeremiah",52),
            ("lamentations",5),
            ("baruch",6),
            ("ezekiel",48),
            ("daniel",14),
            ("hosea",14),
            ("joel",4),
            ("amos",9),
            ("obadiah",1),
            ("jonah",4),
            ("micah",7),
            ("nahum",3),
            ("habakkuk",3),
            ("zephaniah",3),
            ("haggai",2),
            ("zechariah",14),
            ("malachi",3),
            ("matthew",28),
            ("mark",16),
            ("luke",24),
            ("john",21),
            ("acts",28),
            ("romans",16),
            ("1corinthians",16),
            ("2corinthians",13),
            ("galatians",6),
            ("ephesians",6),
            ("philippians",4),
            ("colossians",4),
            ("1thessalonians",5),
            ("2thessalonians",3),
            ("1timothy",6),
            ("2timothy",4),
            ("titus",3),
            ("philemon",1),
            ("hebrews",13),
            ("james",5),
            ("1peter",5),
            ("2peter",3),
            ("1john",5),
            ("2john",1),
            ("3john",1),
            ("jude",1),
            ("revelation",22),
            )
#++++++++++++++++ Bible extraction functions ++++++++++++++++

def get_bible_chapter(book_name="preface", chapter_number = "0"):
    print("getting", book_name, "chapter", chapter_number)
    try:
        with urlopen(SITE + book_name + '/' + chapter_number) as wbpg:
            html = wbpg.read()
    except:
        return None
    h = html.decode("utf-8")
    #print("raw html ", len(h), "chars")
    c = extract_contents(h, 'div class="content"')[0]
    #print("page content", len(c), "chars")
    t = extract_contents(c, 'li class="pager__item is-active"')
    if len(t) > 1:
        if t[0] != t[1]: print('mismatched title',t)
    else: print('Title not found', book_name, i)
    txt = cln(extract_contents(c, 'div class="contentarea"')[0])
    print("got", len(txt), "characters")
    return txt


def get_bible_book(book_name="preface", number_of_chapters = 0):
    book = ""
    for i in range(number_of_chapters+1):
        sleep(choice((144,40,12,3,1)))
        chap = get_bible_chapter(book_name,str(i))
        if chap is None: continue
        if len(chap) < 50: continue
        book += chap
        book += "\n\n"
    return book

def save_book(settings):
    name = settings[0]
    chaps = settings[1]
    h = get_bible_book(name,chaps)
    fnm = name + ".txt"
    f = open(fnm, mode='w',encoding="utf-8")
    f.write(h)
    f.close()
    print("saved",fnm)

for info in allbooks[2:]:
    save_book(info)

#h = get_bible_chapter("2samuel",0)
