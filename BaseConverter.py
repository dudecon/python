#!python
# dozinal.py
# This code converts between arbitrary numeric "base" or radix
# originally designed for Dozinal (base 12) it now handles bases from 2 to 1234
# it also does decimal places! 

BASE = 12
PREC = 8
GLYPHS = []
VERBOSE = False

def compute_glyphs(BASE):
    GLYPHS = []
    BASE = min(BASE,1234)
    offset = 55
    for i in range(BASE):
        if i < 10:
            GLYPHS.append(str(i))
            continue
        if i == 36: offset += 101
        elif i+offset == 888: offset += 2
        elif i+offset == 896: offset += 5
        elif i+offset == 907: offset += 4
        elif i+offset == 930: offset += 2
        elif i+offset == 1328: offset += 2
        elif i+offset == 1367: offset += 11
        GLYPHS.append(chr(i+offset))
    return GLYPHS

def rebase(num):
    global GLYPHS
    if len(GLYPHS) != BASE:
        GLYPHS = compute_glyphs(BASE)
    
    if num < 0:
        sign = '-'
        num = -num
    else: sign = ''
    whole = int(num)
    frac = num - whole

    whole_parts = []
    frac_parts = []
    prec = PREC
    while prec > 0:
        prec -= 1
        frac *= BASE

        part = int(frac)
        frac -= part
        if part == 0: break

        frac_parts.append(GLYPHS[part])

    while whole > 0:
        mod = whole % BASE
        whole = whole // BASE
        whole_parts.append(GLYPHS[mod])
        
    if len(whole_parts) == 0:
        whole_parts.append(GLYPHS[0])
    if len(frac_parts) == 0:
        return sign + "".join(reversed(whole_parts))

    return sign + "{}.{}".format("".join(reversed(whole_parts)),
                  "".join(frac_parts))

def debase(string):
    global GLYPHS
    if len(GLYPHS) != BASE:
        GLYPHS = compute_glyphs(BASE)
    VALUES = {}
    for i in range(len(GLYPHS)):
        VALUES[GLYPHS[i]] = i
    
    if string[0] == '-':
        negative = True
        string = string[1:]
    else: negative = False
    try:
        whole_parts, frac_parts = string.split(".")
    except:
        whole_parts = string
        frac_parts = ''

    whole = 0

    for idx in range(len(whole_parts)):
        whole += VALUES[whole_parts[idx]]
        if idx < len(whole_parts) - 1:
            whole *= BASE

    frac = 0
    max_idx = len(frac_parts) - 1

    for idx in range(len(frac_parts)):
        part = frac_parts[max_idx - idx]
        frac += VALUES[part] / BASE

        if idx < max_idx:
            frac /= BASE

    result = whole + round(frac,PREC)
    if negative: return -result
    return result

def b(radix):
    global BASE, GLYPHS
    if radix < 2:
        print("Fallback to binary")
        BASE = 2
    else:
        BASE = int(radix)
    GLYPHS = compute_glyphs(BASE)
    if VERBOSE: print(GLYPHS)

if __name__ == '__main__':
    TestConvert = 808888888888888888888888888888888888888888888888888888888888888888888888811118888888118888888888888111111111118811188888888888811111188888881111888888888888111188888888111111188888888888111888888811188111188888888888111888881118888811188888888888111188888888888111888888888888811188888888111111888888888888111811111111111188888888888811888881111111188888888888888888888888888888888888888888888888888888888888888888888881
    for i in range(400,440):
        b(i)
        TestConversion = rebase(TestConvert)
        ConvLen = len(TestConversion)
        print("{} converted to base {} is {} digits long: ".format(TestConvert,BASE,ConvLen), TestConversion)
    ConvertedBack = debase(TestConversion)
    print("{} in base {} is".format(TestConvert,BASE), ConvertedBack, "in decimal")
    if TestConvert == ConvertedBack: print("success!")
    else: print("Something went wrong")
    print("Call b(base) to set the radix base,\nand PREC to set the precision.\nCall rebase() to convert,\nand debase() to convert back to decimal.")
