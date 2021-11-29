#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# wiktionary random character page
# Open a new browser tab with a random character from UTF
import os, webbrowser, sys, codecs
from random import choice

# append the page number on the end of this address
pre_address = "http://en.wiktionary.org/wiki/"
# the last page number (inclusive), page numbers start at 1
character_last = 12000

random_character_number = choice(range(0, character_last + 1))
print(random_character_number)
print(sys.path)
full_address = pre_address + chr(random_character_number)

# This no longer works in the command line
#print(full_address)

webbrowser.open(full_address, new=2)

#also open the Unicode chart
general_address = "http://www.unicode.org/charts/PDF/U{0}.pdf"
hex_address = (hex(random_character_number)[2:-2] + "00").upper()
while len(hex_address) < 4: hex_address = "0" + hex_address
full_unicode_chart_address = general_address.format(hex_address)
webbrowser.open(full_unicode_chart_address, new=2)
