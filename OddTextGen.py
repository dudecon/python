# Similar letter substituter
# To make text look a bit strange

from random import choice
from time import sleep
from TextOddifier import oddify
from SlowPrint import sprint

SLDVals = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890++--**/?.,<>}{()^%$#@!;:"

def strgen(howlong=45):
    s = ''
    for i in range(howlong):
        s += choice(SLDVals)
    return s

while True:
    sprint(oddify(strgen( choice(( 45, 12, 33,17,48)) )), choice(( .01, .01618, .002618)) )

