# Suno Time Adder
# Adds up all the durations of music in a Suno playlist

SITE = "https://suno.com/playlist/2cf0cd7b-e48e-492d-ad6c-20e1f2182923"
DEBUG = True

from urllib.request import urlopen, Request
import webbrowser
from HTML_Cleaner import *

def get_webpage_data(site=SITE):
    print("fetching", site)
    try:
        req = Request(site, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'})
        with urlopen(req) as wbpg:
            html = wbpg.read()
    except:
        print('fetch failed')
        raise
        return None
    h = html.decode("utf-8")
    if DEBUG: print("raw html ", len(h), "chars")
    c = extract_contents(h, 'div class="react-aria-GridList"')[0]
    if DEBUG: print("page content", len(c), "chars")
    tstmps = extract_contents(c, 'span class="flex absolute bottom-[2px] items-center right-[2px] text-[11px]')
    print("got", len(tstmps), "timestamps")
    return tstmps

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
        timestamp_label = f"{days}d {hours}:{minutes:02}:{seconds:02}"
    elif hours > 0:
        timestamp_label = f"{hours}:{minutes:02}:{seconds:02}"
    else:
        timestamp_label = f"{minutes:02}:{seconds:02}"

    return timestamp_label

def sum_timestamps(tstmps):
    total = 0
    for tst in tstmps:
        total += find_seconds(tst)
    return total

if __name__ == '__main__':
    tstmps = get_webpage_data()
    if tstmps:
        total_seconds = sum_timestamps(tstmps)
        formatted_total = generate_timestamp(total_seconds)
        print("Total duration:", formatted_total)
    input("enter to exit")
