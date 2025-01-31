# HTML Processing Utility Functions

DEBUG = False

def find_tag_bounds(html, tag):
    """
    Find the bounds of all occurrences of a given HTML tag in the provided HTML string.

    Args:
        html (str): The HTML content to search through.
        tag (str): The tag to find (e.g., "div", "p").

    Returns:
        list: A list of tuples, where each tuple contains the start and end positions of the tag content.
    """
    # Use for nested tags
    # To remove the tags themselves, use tgx()
    tag_label = tag.split()[0]
    start_tag = f"<{tag}"  # Specific tag with attributes at depth 0
    all_start = f"<{tag_label}"  # Any tag of this type for nested checks
    end_tag = f"</{tag_label}>"
    if DEBUG:
        print("finding", tag)
        print("start tag ", start_tag)
        print("all start tag ", all_start)
        print("end tag ", end_tag)

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
            end_search_start = pos  # and search for the end tag from the same point

        # if DEBUG: print("depth", depth, "start", start_pos)

        end_pos = html.find(end_tag, end_search_start)
        # if DEBUG: print("depth", depth, "end", end_pos)

        if end_pos == -1:
            # Close out the current bounds with the end of file and return everything
            thisbound.append(len(html) - 1)
            bounds.append(thisbound)
            return bounds

        if (start_pos < end_pos) and not (start_pos == -1):
            # Found another start, before the next end tag
            pos = html.find('>', start_pos) + 1
            depth += 1
            continue
        else:
            # Found an end tag before the next start tag
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
    """
    Extract the content between all occurrences of a given HTML tag.

    Args:
        html (str): The HTML content to search through.
        tag (str): The tag to extract content from (e.g., "div", "p").

    Returns:
        list: A list of strings, where each string is the content between the tags.
    """
    bounds = find_tag_bounds(html, tag)
    if DEBUG:
        print("bounds", bounds)
    if len(bounds):
        contents = [html[html.find('>', start) + 1:end].strip() for start, end in bounds]
        return contents
    else:
        return []  # Return an empty list if no bounds were found

def excise_content(html, tag):
    """
    Remove all occurrences of a given HTML tag and its content.

    Args:
        html (str): The HTML content to modify.
        tag (str): The tag to remove (e.g., "div", "p").

    Returns:
        str: The HTML content with the specified tags removed.
    """
    tag_label = tag.split()[0]
    end_tag = f"</{tag_label}>"
    bounds = find_tag_bounds(html, tag)
    # Process bounds from last to first to avoid messing up the indices
    for start, end in reversed(bounds):
        html = html[:start] + html[end + len(end_tag):]
    return html

def tgx(st, strt, endt):
    """
    Excise all text between all occurrences of the specified tag pairs.

    Args:
        st (str): The string to modify.
        strt (str): The start tag.
        endt (str): The end tag.

    Returns:
        str: The modified string with text between tag pairs removed.
    """
    while True:
        stpos = st.find(strt)
        if stpos == -1:
            break
        edpos = st.find(endt, stpos)
        if edpos == -1:
            break
        edpos += len(endt)
        st = st[:stpos] + st[edpos:]
    return st

def cln(st):
    """
    Clean out markup elements from the provided HTML string.

    Args:
        st (str): The HTML content to clean.

    Returns:
        str: The cleaned HTML content.
    """
    # Markup elements to remove or replace
    precull = ('\t',)
    excice = ('header', 'head', 'script', 'footer', 'sup', 'noscript', 'nav', 'form',
              'cite', 'ol', 'style', 'span class="bcv"',
              'semantics', 'math')
    detag = ('html', 'div', 'body', '!DOCTYPE', 'a', '!--', 'img', 'style',
             'li', 'td', 'ul', 'tr', 'tbody', 'table', 'h1', 'h2', 'h3', 'h4',
             'span', 'th', 'p', 'i', 'b', 'small', 'label', 'dd', 'dl', 'dt', 'blockquote',
             'center', 'main', 'figure', 'figcaption', 'meta')
    postcull = ('</abbr>', '[edit]')
    replacement = (('&lt;', '<'), ('&gt;', '>'), ('&amp;', '&'),
                   ('&euro;', '€'), ('&pound;', '£'), ('&quot;', '"'), ('&apos;', "'"),
                   ('&nbsp;', ' '), ('&ensp;', ' '), ('&emsp;', ' '), ('&emsp13;', ' '),
                   ('&numsp;', ' '), ('&puncsp;', ' '), ('&thinsp;', ' '), ('&hairsp;', ' '),
                   ('  ', ' '), (' \n', '\n'), ('\n\n', '\n'),
                   )
    # Remove specific elements
    for tg in precull:
        if DEBUG:
            print(len(st))
        if DEBUG:
            print(tg)
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
