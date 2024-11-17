#Suno Time Adder
# Adds up all the durations of music in a Suno playlist

SITE = "https://suno.com/playlist/2cf0cd7b-e48e-492d-ad6c-20e1f2182923"
DEBUG = True

from urllib.request import urlopen
import webbrowser
from HTML_Cleaner import *

def get_webpage_data(site = SITE):
    print("fetching", site)
    try:
        with urlopen(site) as wbpg:
            html = wbpg.read()
    except:
        if DEBUG:
            print('fetch failed')
            raise
        return None
    h = html.decode("utf-8")
    if DEBUG: print("raw html ", len(h), "chars")
    c = extract_contents(h, 'div class="react-aria-GridList"')[0]
    if DEBUG: print("page content", len(c), "chars")
    tstmps = extract_contents(c, 'span class="flex absolute bottom-[2px] items-center right-[2px] text-[11px]')
    print("got", len(tstmp), "timestamps")
    return tstmp


def find_seconds(timestamp_label):
    total_secs = 0
    digits = timestamp_label.split(':')
    i = 0
    while len(digits) > 0:
        total_secs += (60**i) * int(digits.pop())
        i += 1
    return total_secs

def generate_timestamp(seconds):
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    if days > 0:
        timestamp_label = f"{days}d {hours:02}:{minutes:02}:{seconds:02}"
    elif hours > 0:
        timestamp_label = f"{hours:02}:{minutes:02}:{seconds:02}"
    else:
        timestamp_label = f"{minutes:02}:{seconds:02}"

    return timestamp_label

def sum_timestamps(tstmps):
    total = 0
    for tst in tstmps:
        total += find_seconds(tst)
    return total

if __name__ == '__main__':
    get_webpage_data()
    input("enter to exit")

