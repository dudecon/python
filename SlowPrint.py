# Prints stuff out, but not so fast

from time import sleep

def sprint(page, delayfactor = 0.0035):
    for ln in page.split('\n'):
        ln = ln.strip()
        if len(ln) == 0: continue
        if ln.find(' ') == -1:
            for thing in ln:
                print(thing, end='', flush=True)
                sleep(delayfactor/6)
        else:
            for thing in ln.split(' '):
                print(thing, end=' ', flush=True)
                sleep(delayfactor)
        print('')  # for the newline
        sleep((len(ln) + 5) * (delayfactor * 1.618))

if __name__ == '__main__':
    sprint("This is a demonstration of the terrible power\nof this function.",0.01)
