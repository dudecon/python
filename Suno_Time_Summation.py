# Suno Time Adder
# Adds up song durations in Suno playlists, indexes a profile playlist page,
# and writes an HTML catalog of Bible playlists for peripheralarbor.com.

DEBUG = True
HANDLE = "dudecon"
HTML_OUT = "suno_bible_playlists.htm"

# Optional: sum only these playlist IDs instead of indexing a profile.
albums = []
# albums = ["2cf0cd7b-e48e-492d-ad6c-20e1f2182923", "aa8b969d-9d94-45bf-8c61-0d140af88fac"]  # Bible 1 and 2

API_BASE = "https://studio-api.prod.suno.com"
SUNO_SITE = "https://suno.com"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

from html import escape
from json import dumps, loads
from time import sleep
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

# Catholic canon order for book-named playlists. Compilations sort first.
CANON_ORDER = [
    "genesis", "exodus", "leviticus", "numbers", "deuteronomy", "joshua",
    "judges", "ruth", "1 samuel", "2 samuel", "1 kings", "2 kings",
    "1 chronicles", "2 chronicles", "ezra", "nehemiah", "tobit", "judith",
    "esther", "1 maccabees", "2 maccabees", "job", "psalms", "proverbs",
    "ecclesiastes", "song of songs", "song of solomon", "wisdom", "sirach",
    "isaiah", "jeremiah", "lamentations", "baruch", "ezekiel", "daniel",
    "hosea", "joel", "amos", "obadiah", "jonah", "micah", "nahum",
    "habakkuk", "zephaniah", "haggai", "zechariah", "malachi",
    "matthew", "mark", "luke", "john", "acts", "romans",
    "1 corinthians", "first letter to the corinthians",
    "2 corinthians", "second letter to the corinthians", "book of 2 corinthians",
    "galatians", "ephesians", "philippians", "colossians",
    "1 thessalonians", "2 thessalonians", "1 timothy", "2 timothy",
    "titus", "philemon", "hebrews", "james", "1 peter", "2 peter",
    "1 john", "2 john", "3 john", "jude", "revelation",
]

BIBLE_MARKERS = set(CANON_ORDER) | {
    "bible", "scripture", "gospel", "psalm", "psalms",
    "old testament", "new testament", "nab",
}

# Display names in Catholic canon order, used to list compilation contents.
BOOK_CANON = [
    "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua",
    "Judges", "Ruth", "1 Samuel", "2 Samuel", "1 Kings", "2 Kings",
    "1 Chronicles", "2 Chronicles", "Ezra", "Nehemiah", "Tobit", "Judith",
    "Esther", "1 Maccabees", "2 Maccabees", "Job", "Psalms", "Proverbs",
    "Ecclesiastes", "Song of Songs", "Wisdom", "Sirach", "Isaiah",
    "Jeremiah", "Lamentations", "Baruch", "Ezekiel", "Daniel", "Hosea",
    "Joel", "Amos", "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk",
    "Zephaniah", "Haggai", "Zechariah", "Malachi", "Matthew", "Mark",
    "Luke", "John", "Acts", "Romans", "1 Corinthians", "2 Corinthians",
    "Galatians", "Ephesians", "Philippians", "Colossians",
    "1 Thessalonians", "2 Thessalonians", "1 Timothy", "2 Timothy",
    "Titus", "Philemon", "Hebrews", "James", "1 Peter", "2 Peter",
    "1 John", "2 John", "3 John", "Jude", "Revelation",
]

# Cryptic song titles that do not name their book.
TITLE_BOOK_HINTS = {
    "the seven spirits": "Jeremiah",
    "the seven praises": "Jeremiah",
    "the aramean ambush": "2 Kings",
    "the stars": "Revelation",
    "a prayer for a godly wife": "Proverbs",
    "gifts for the tent of meeting": "Numbers",
    "bible pants": "Exodus",
    "lament for saul and his son jonathan": "2 Samuel",
    "seven flaming torches, horns, and eyes": "Revelation",
}

# Text links from https://peripheralarbor.com/Bible/ (relative to /Bible/).
KJV_TEXT_LINKS = [
    ("kjv_no_verse.html", "Holy Bible"),
    ("kjv.txt", "KJV textfile 930105"),
    ("BibleParser.py", "Bible parser script"),
    ("kjv_Ge.htm", "The Book of Genesis"),
    ("kjv_Exo.htm", "The Book of Exodus"),
    ("kjv_Lev.htm", "The Book of Leviticus"),
    ("kjv_Num.htm", "The Book of Numbers"),
    ("kjv_Deu.htm", "The Book of Deuteronomy"),
    ("kjv_Josh.htm", "The Book of Joshua"),
    ("kjv_Jdgs.htm", "The Book of Judges"),
    ("kjv_Ruth.htm", "The Book of Ruth"),
    ("kjv_1Sm.htm", "The Book of First Samuel"),
    ("kjv_2Sm.htm", "The Book of Second Samuel"),
    ("kjv_1Ki.htm", "The Book of First Kings"),
    ("kjv_2Ki.htm", "The Book of Second Kings"),
    ("kjv_1Chr.htm", "The Book of First Chronicles"),
    ("kjv_2Chr.htm", "The Book of Second Chronicles"),
    ("kjv_Ezra.htm", "The Book of Ezra"),
    ("kjv_Neh.htm", "The Book of Nehemiah"),
    ("kjv_Est.htm", "The Book of Esther"),
    ("kjv_Job.htm", "The Book of Job"),
    ("kjv_Psa.htm", "The Book of Psalms"),
    ("kjv_Prv.htm", "The Book of Proverbs"),
    ("kjv_Eccl.htm", "The Book of Ecclesiastes"),
    ("kjv_SSol.htm", "The Book of Song of Songs"),
    ("kjv_Isa.htm", "The Book of Isaiah"),
    ("kjv_Jer.htm", "The Book of Jeremiah"),
    ("kjv_Lam.htm", "The Book of Lamentation"),
    ("kjv_Eze.htm", "The Book of Ezekiel"),
    ("kjv_Dan.htm", "The Book of Daniel"),
    ("kjv_Hos.htm", "The Book of Hosea"),
    ("kjv_Joel.htm", "The Book of Joel"),
    ("kjv_Amos.htm", "The Book of Amos"),
    ("kjv_Obad.htm", "The Book of Obadiah"),
    ("kjv_Jonah.htm", "The Book of Jonah"),
    ("kjv_Mic.htm", "The Book of Micah"),
    ("kjv_Nahum.htm", "The Book of Nahum"),
    ("kjv_Hab.htm", "The Book of Habakkuk"),
    ("kjv_Zep.htm", "The Book of Zephaniah"),
    ("kjv_Hag.htm", "The Book of Haggai"),
    ("kjv_Zec.htm", "The Book of Zechariah"),
    ("kjv_Mal.htm", "The Book of Malachi"),
    ("kjv_Mat.htm", "The Book of Matthew"),
    ("kjv_Mark.htm", "The Book of Mark"),
    ("kjv_Luke.htm", "The Book of Luke"),
    ("kjv_John.htm", "The Book of John"),
    ("kjv_Acts.htm", "The Book of Acts"),
    ("kjv_Rom.htm", "The Book of Romans"),
    ("kjv_1Cor.htm", "The Book of First Corinthians"),
    ("kjv_2Cor.htm", "The Book of Second Corinthians"),
    ("kjv_Gal.htm", "The Book of Galatians"),
    ("kjv_Eph.htm", "The Book of Ephesians"),
    ("kjv_Phi.htm", "The Book of Philippians"),
    ("kjv_Col.htm", "The Book of Colossians"),
    ("kjv_1Th.htm", "The Book of First Thessalonians"),
    ("kjv_2Th.htm", "The Book of Second Thessalonians"),
    ("kjv_1Tim.htm", "The Book of First Timothy"),
    ("kjv_2Tim.htm", "The Book of Second Timothy"),
    ("kjv_Titus.htm", "The Book of Titus"),
    ("kjv_Phmn.htm", "The Book of Philemon"),
    ("kjv_Heb.htm", "The Book of Hebrews"),
    ("kjv_Jas.htm", "The Book of James"),
    ("kjv_1Pet.htm", "The Book of First Peter"),
    ("kjv_2Pet.htm", "The Book of Second Peter"),
    ("kjv_1Jn.htm", "The Book of First John"),
    ("kjv_2Jn.htm", "The Book of Second John"),
    ("kjv_3Jn.htm", "The Book of Third John"),
    ("kjv_Jude.htm", "The Book of Jude"),
    ("kjv_Rev.htm", "The Book of Revelation"),
]


def kjv_text_links_html():
    lines = ['<h2>KJV Bible Text</h2>', '<p><a href="/Bible/">Bible Index</a></p>']
    for href, label in KJV_TEXT_LINKS:
        lines.append(f'<p><a href="/Bible/{href}">{escape(label)}</a></p>')
    lines.append('<p><a href="http://bible.tryop.com">Barebones Holy Bible — bible.tryop.com</a></p>')
    return "\n".join(lines)


def api_request(url, payload=None, retries=5):
    """GET JSON, or POST JSON if payload is a dict. Retries rate limits."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
        "Origin": SUNO_SITE,
        "Referer": f"{SUNO_SITE}/",
    }
    data = None
    if payload is not None:
        headers["Content-Type"] = "application/json"
        data = dumps(payload).encode("utf-8")
    delay = 2
    for attempt in range(retries):
        req = Request(url, headers=headers, data=data, method="POST" if data else "GET")
        try:
            with urlopen(req, timeout=60) as resp:
                raw = resp.read()
            return loads(raw.decode("utf-8"))
        except HTTPError as err:
            body = err.read()
            if err.code in (429, 500, 502, 503) and attempt < retries - 1:
                if DEBUG:
                    print(f"  {err.code} on {url} — retry in {delay}s")
                sleep(delay)
                delay = min(delay * 2, 30)
                continue
            raise RuntimeError(f"HTTP {err.code} for {url}: {body[:300]!r}") from err
        except URLError as err:
            if attempt < retries - 1:
                sleep(delay)
                delay = min(delay * 2, 30)
                continue
            raise RuntimeError(f"request failed for {url}: {err}") from err
    raise RuntimeError(f"request failed for {url}")


def find_seconds(timestamp_label):
    total_secs = 0
    digits = timestamp_label.split(":")
    i = 0
    while len(digits) > 0:
        total_secs += (60 ** i) * int(digits.pop())
        i += 1
    return total_secs


def generate_timestamp(seconds):
    seconds = int(round(seconds or 0))
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    if days > 0:
        return f"{days}d {hours}:{minutes:02}:{seconds:02}"
    if hours > 0:
        return f"{hours}:{minutes:02}:{seconds:02}"
    return f"{minutes:02}:{seconds:02}"


def clip_duration(clip):
    if not clip:
        return 0.0
    meta = clip.get("metadata") or {}
    dur = meta.get("duration")
    if dur is None:
        dur = clip.get("duration")
    try:
        return float(dur or 0)
    except (TypeError, ValueError):
        return 0.0


def fetch_playlist(playlist_id):
    """Full playlist: name, description, clips, summed duration."""
    clips = []
    meta = {}
    page = 1
    total = None
    while page <= 50:
        if DEBUG:
            print("fetching playlist", playlist_id, "page", page)
        data = api_request(f"{API_BASE}/api/playlist/{playlist_id}/?page={page}")
        meta = {k: v for k, v in data.items() if k != "playlist_clips"}
        batch = data.get("playlist_clips") or []
        clips.extend(batch)
        total = data.get("num_total_results")
        if not batch or (total is not None and len(clips) >= total):
            break
        page += 1
        sleep(0.3)
    seconds = 0.0
    for item in clips:
        seconds += clip_duration(item.get("clip") if isinstance(item, dict) else None)
    if not seconds:
        try:
            seconds = float(meta.get("total_duration") or 0)
        except (TypeError, ValueError):
            seconds = 0.0
    song_count = meta.get("num_total_results") or meta.get("song_count") or len(clips)
    titles = []
    for item in clips:
        clip = item.get("clip") if isinstance(item, dict) else None
        title = (clip or {}).get("title") or ""
        if title:
            titles.append(title)
    return {
        "id": meta.get("id") or playlist_id,
        "name": meta.get("name") or "Untitled playlist",
        "description": (meta.get("description") or "").strip(),
        "image_url": meta.get("image_url") or "",
        "song_count": int(song_count or 0),
        "seconds": seconds,
        "url": f"{SUNO_SITE}/playlist/{playlist_id}",
        "is_public": meta.get("is_public"),
        "titles": titles,
    }


def fetch_profile(handle):
    if DEBUG:
        print("fetching profile", handle)
    return api_request(
        f"{API_BASE}/api/profiles/{handle}"
        "?playlists_sort_by=created_at&clips_sort_by=created_at"
    )


def fetch_profile_playlists(handle, user_id=None):
    """All public playlists from a profile page, via the user_playlists feed."""
    if not user_id:
        profile = fetch_profile(handle)
        user_id = profile.get("user_id")
    items = []
    cursor = None
    for _ in range(20):
        if DEBUG:
            print("fetching user_playlists cursor", cursor)
        data = api_request(
            f"{API_BASE}/api/unified/feed",
            payload={
                "feed_id": "user_playlists",
                "cursor": cursor,
                "page_size": 50,
                "target_user_id": user_id,
            },
        )
        feed = data.get("feed") or {}
        batch = feed.get("items") or []
        items.extend(batch)
        cursor = feed.get("next_cursor")
        if not cursor or not batch:
            break
        sleep(0.3)
    playlists = []
    seen = set()
    for item in items:
        info = item.get("content_item") or {}
        pid = info.get("playlist_id") or item.get("content_id")
        if not pid or pid in seen:
            continue
        seen.add(pid)
        playlists.append({
            "id": pid,
            "name": info.get("playlist_name") or "Untitled playlist",
            "song_count": info.get("playlist_song_count") or 0,
            "image_url": info.get("playlist_image_url") or "",
            "url": f"{SUNO_SITE}/playlist/{pid}",
        })
    return playlists


def normalize_title(name):
    text = (name or "").lower()
    for prefix in ("the book of ", "book of ", "the "):
        if text.startswith(prefix):
            text = text[len(prefix):]
    text = text.replace("first letter to the ", "1 ")
    text = text.replace("second letter to the ", "2 ")
    text = text.replace("letter to the ", "")
    return " ".join(text.split())


def is_bible_playlist(playlist):
    blob = f"{playlist.get('name', '')} {playlist.get('description', '')}".lower()
    if any(marker in blob for marker in BIBLE_MARKERS):
        return True
    title = normalize_title(playlist.get("name"))
    return title in BIBLE_MARKERS or any(title.startswith(m) for m in CANON_ORDER)


def bible_sort_key(playlist):
    name = playlist.get("name") or ""
    title = normalize_title(name)
    if "bible" in name.lower():
        digits = "".join(ch if ch.isdigit() else " " for ch in name)
        nums = [int(n) for n in digits.split() if n]
        album_n = nums[0] if nums else 0
        return (0, album_n, title)
    for i, book in enumerate(CANON_ORDER):
        if title == book or title.startswith(book + " "):
            return (1, i, title)
    return (2, 999, title)


def fallback_description(playlist):
    name = playlist.get("name") or "this playlist"
    return f"Songs drawn from {name}, set to music on Suno."


def is_compilation_album(playlist):
    return "bible" in (playlist.get("name") or "").lower()


def _fold(text):
    return " ".join("".join(ch.lower() if ch.isalnum() else " " for ch in (text or "")).split())


def _aliases_for_book(display):
    n = display.lower()
    aliases = [n, f"book of {n}", f"the book of {n}"]
    if n.startswith(("1 ", "2 ", "3 ")):
        ordinal = {"1 ": "first", "2 ": "second", "3 ": "third"}[n[:2]]
        rest = n[2:]
        aliases += [
            f"{n}", f"{ordinal} {rest}",
            f"{ordinal} letter to {rest}", f"{ordinal} letter to the {rest}",
            f"{ordinal} letter of {rest}",
            f"the {ordinal} letter to {rest}", f"the {ordinal} letter to the {rest}",
            f"the {ordinal} letter of {rest}",
            f"letter to {rest}", f"letter to the {rest}",
            f"book of {n}", f"book of {ordinal} {rest}",
        ]
        if n == "1 chronicles":
            aliases.append("chronicles")
    else:
        aliases += [
            f"letter to the {n}", f"letter to {n}",
            f"the letter to the {n}", f"the letter to {n}",
            f"letter of {n}", f"the letter of {n}",
        ]
    if n == "psalms":
        aliases.append("psalm")
    if n == "sirach":
        aliases += ["ben sirah", "ben sira", "ecclesiasticus"]
    if n == "song of songs":
        aliases.append("song of solomon")
    return aliases


_ALIAS_TO_BOOK = []
for _book in BOOK_CANON:
    for _alias in _aliases_for_book(_book):
        _ALIAS_TO_BOOK.append((_fold(_alias), _book))
_ALIAS_TO_BOOK.sort(key=lambda item: len(item[0]), reverse=True)


def book_from_title(title):
    folded = _fold(title)
    if not folded:
        return None
    for hint_title, hinted in TITLE_BOOK_HINTS.items():
        if _fold(hint_title) == folded:
            return hinted
    # Catholic Baruch includes the Letter of Jeremiah and a "Praise of Wisdom" chapter.
    if f" baruch " in f" {folded} ":
        return "Baruch"
    padded = f" {folded} "
    best = None
    best_len = 0
    for alias, book in _ALIAS_TO_BOOK:
        if len(alias) <= best_len:
            continue
        if f" {alias} " in padded:
            best = book
            best_len = len(alias)
    return best


def _canon_sort(names):
    order = {name: i for i, name in enumerate(BOOK_CANON)}
    return sorted(names, key=lambda name: order.get(name, 999))


def hinted_book(title):
    folded = _fold(title)
    for hint_title, book in TITLE_BOOK_HINTS.items():
        if _fold(hint_title) == folded:
            return book
    return None


def books_from_titles(titles):
    found = []
    seen = set()
    for title in titles or []:
        book = book_from_title(title)
        if book and book not in seen:
            seen.add(book)
            found.append(book)
    return _canon_sort(found)


def classify_compilation_books(titles):
    """Named book-title songs are full books; cryptic titles are selections."""
    full = set()
    selections = set()
    for title in titles or []:
        hinted = hinted_book(title)
        if hinted:
            selections.add(hinted)
            continue
        book = book_from_title(title)
        if book:
            full.add(book)
    selections -= full
    return _canon_sort(full), _canon_sort(selections)


def compilation_description(playlist):
    base = (playlist.get("description") or "").strip() or fallback_description(playlist)
    lines = [
        line for line in base.splitlines()
        if not line.startswith("Books included:") and not line.startswith("Selections from:")
    ]
    base = "\n".join(lines).strip() or fallback_description(playlist)
    full, selections = classify_compilation_books(playlist.get("titles") or [])
    parts = [base]
    if full:
        parts.append("Books included: " + ", ".join(full) + ".")
    if selections:
        parts.append("Selections from: " + ", ".join(selections) + ".")
    return "\n".join(parts)


def write_html(path, handle, playlists, profile=None):
    total_songs = sum(p["song_count"] for p in playlists)
    total_seconds = sum(p["seconds"] for p in playlists)
    display = (profile or {}).get("display_name") or handle
    bio = ((profile or {}).get("profile_description") or "").strip()
    profile_url = f"{SUNO_SITE}/@{handle}?page=playlists"
    rows = []
    for p in playlists:
        desc = p.get("description") or fallback_description(p)
        img = ""
        if p.get("image_url"):
            img = (
                f'<a href="{escape(p["url"])}">'
                f'<img src="{escape(p["image_url"])}" alt="{escape(p["name"])} cover" '
                f'width="120" height="120" style="float: left; margin: 0 12px 8px 0; '
                f'border: 3px solid #333;"/></a>\n'
            )
        rows.append(
            f'''<div style="clear: both; overflow: hidden; margin: 1.2em 0 1.6em 0;">
{img}<h3 style="margin-top: 0;"><a href="{escape(p["url"])}">{escape(p["name"])}</a></h3>
<p>{escape(desc).replace(chr(10), "<br>")}
<br><b>{p["song_count"]} songs</b> — <b>{escape(generate_timestamp(p["seconds"]))}</b>
</p>
</div>
'''
        )
    html = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<title>Suno Bible Playlists</title>
<link rel="stylesheet" type="text/css" href="/style.css" />
</head>
<body style="background-color: #ece6d8;
	color: #222222;
	font-family: monospace, Sans-serif;
	font-size: 14px;
	cursor:default;">

<div style="opacity: .2; z-index: 1;"><div style="position: absolute;">
<img width="300" alt="Index Picture, left" height="970" src="/PeripheraLeft.png" border="0" style="float: left; margin-top: 50px;" /></div>
<div style="position: absolute; width: 100%;">
<img width="300" alt="Index Picture, right" height="970" src="/PeripheraLight.png" border="0" style="float: right; margin-top: 50px;" /></div>
</div>
<div style="width: 800px; margin: auto; position: relative; z-index: 2;">

<h2>Suno Bible Playlists</h2>
<p>Scripture set to music on <a href="{escape(profile_url)}">Suno by {escape(display)}</a>.
Each playlist is a book or collection whose lyrics are drawn from the Bible
(NAB and related Catholic translations where noted on Suno).</p>
<p>{escape(bio)}</p>
<p><b>{len(playlists)} playlists</b>, <b>{total_songs} songs</b>,
total length <b>{escape(generate_timestamp(total_seconds))}</b>.</p>
<h3></h3>
{''.join(rows)}
{kjv_text_links_html()}
<h2>Navigation Links</h2>
<p><a href="{escape(profile_url)}">All Suno playlists for @{escape(handle)}</a></p>
<a href="/Bible/"><h3>Level Up to Bible</h3></a>
<a href="/"><h3>Back to Peripheral Arbor Homepage</h3></a>
</div>
</body>
</html>
'''
    with open(path, "w", encoding="utf-8") as out:
        out.write(html)
    if DEBUG:
        print("wrote", path)


def print_index(playlists, label):
    print(f"\n{label}: {len(playlists)} playlists")
    total_seconds = 0
    total_songs = 0
    for p in playlists:
        total_seconds += p["seconds"]
        total_songs += p["song_count"]
        print(
            f"  {p['name']}: {p['song_count']} songs, "
            f"{generate_timestamp(p['seconds'])}  {p['url']}"
        )
        if p.get("description"):
            first = p["description"].splitlines()[0]
            print(f"    {first[:120]}")
    print(
        f"Total: {total_songs} songs, {generate_timestamp(total_seconds)} "
        f"({int(round(total_seconds))} seconds)"
    )
    return total_seconds


if __name__ == "__main__":
    profile = None
    if albums:
        ids = albums
        print("summing", len(ids), "listed playlist(s)")
        detailed = []
        for pid in ids:
            detailed.append(fetch_playlist(pid))
            sleep(0.4)
        print_index(detailed, "Listed playlists")
    else:
        profile = fetch_profile(HANDLE)
        summaries = fetch_profile_playlists(HANDLE, user_id=profile.get("user_id"))
        print("indexed", len(summaries), "playlists from", f"{SUNO_SITE}/@{HANDLE}?page=playlists")
        detailed = []
        for summary in summaries:
            info = fetch_playlist(summary["id"])
            if not info.get("image_url"):
                info["image_url"] = summary.get("image_url") or ""
            if not info.get("song_count"):
                info["song_count"] = summary.get("song_count") or 0
            detailed.append(info)
            sleep(0.4)
        print_index(detailed, f"All @{HANDLE} playlists")
        bible = [p for p in detailed if is_bible_playlist(p)]
        bible.sort(key=bible_sort_key)
        for p in bible:
            if is_compilation_album(p):
                p["description"] = compilation_description(p)
        print_index(bible, "Bible playlists")
        write_html(HTML_OUT, HANDLE, bible, profile=profile)
        print("HTML catalog:", HTML_OUT)
    try:
        input("enter to exit")
    except EOFError:
        pass
