# Mastermind like game

from random import choices, sample
from time import sleep

DUPLICATES = False
NumGlyphs = 36
SeqLen = 4

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


def choose_sequence(seq_len, glyphs):
    if DUPLICATES: seq = ''.join(choices(glyphs, k=seq_len))
    else:
        seq_len = min(seq_len,len(glyphs))
        seq = ''.join( sample(glyphs,   seq_len))
    return seq


def isvalidguess(seq, seq_len, glyphs):
    guess_len = len(seq)
    if guess_len != seq_len:
        print(f"your guess was {guess_len} glyphs long,\n\
but the sequence is {seq_len} long")
        return False
    for gl in seq:
        if gl not in glyphs:
            print(f"your guess contained {gl}\n\
which is not (currently) a valid glyph")
            return False
    return True

helpstr = '''Type stuff to guess the secret sequence
# to show the glyph pool
% to show how many glyphs in your last guess are in the sequence
@ to show which glyphs from your last guess are in the sequence
! to disclose the sequence, and re-roll
+ to set the number of glyphs in the sequence, and re-roll
* to set the size of the glyph pool, and re-roll
^ to toggle duplicate glyphs, does NOT re-roll'''

print(helpstr)
allglyphs = compute_glyphs(NumGlyphs)
secret_sequence = choose_sequence(SeqLen,allglyphs)
lastguess = ''
cmd = '#'
while True:
    if len(cmd) == 0: print(helpstr)
    elif cmd[0] == '#':
        print('the current valid glyph set is as follows:')
        print(''.join(allglyphs))
        print(f'the secret sequence is {SeqLen} glyphs long')
    elif cmd[0] == '%':
        n = 0
        for gl in lastguess:
            if gl in secret_sequence: n += 1
        print(f'your last guess contained {n} correct glyphs')
    elif cmd[0] == '@':
        corgl = ''
        for gl in lastguess:
            if gl in secret_sequence: corgl += gl
        print(f'in your last guess {corgl} are in the sequence')
    elif cmd[0] == '!':
        print(f'the secret sequence was {secret_sequence}')
        secret_sequence = choose_sequence(SeqLen,allglyphs)
    elif cmd[0] == '+':
        try:
            SeqLen = int(input("sequence should be how long? "))
            secret_sequence = choose_sequence(SeqLen,allglyphs)
            SeqLen = len(secret_sequence)
            print(f"sequence is now\n{SeqLen} glyphs long")
        except:
            print(f"errorǃ sequence is still\n{SeqLen} glyphs long")
    elif cmd[0] == '*':
        try:
            NumGlyphs = int(input("how many glyphs? "))
            allglyphs = compute_glyphs(NumGlyphs)
            NumGlyphs = len(allglyphs)
            secret_sequence = choose_sequence(SeqLen,allglyphs)
            SeqLen = len(secret_sequence)
            print(f"there are now\n{NumGlyphs} glyphs")
        except:
            print(f"errorǃ there are still\n{NumGlyphs} glyphs")
    elif cmd[0] == '^':
        if DUPLICATES:
            DUPLICATES = False
            print('no duplicate glyphs allowed in the next sequence')
        else:
            DUPLICATES = True
            print('the next sequence may contain duplicate glyphs')
    elif isvalidguess(cmd, SeqLen, allglyphs):
        lastguess = cmd
        if cmd == secret_sequence:
            print(f"Yes! {cmd} is correct! You win!")
            sleep(.5)
            print('take a moment to celebrate your victory')
            sleep(1)
            print('Okay. New sequence generated.')
            secret_sequence = choose_sequence(SeqLen,allglyphs)
            sleep(.5)
            print('On with the game!')
        else: print('sorry, try again')
    else: print(helpstr)
    cmd = input('-> ')
