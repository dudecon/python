# Name generator
from random import choice
Phonems = ('a', 'ja', 'de', 'na', 't', 'ef', 'it', 'el','um','ja','lij','ma','qej','ur','ah')

def randname(sylables):
    result = ""
    for i in range(sylables):
        result += choice(Phonems)
    return result
