# HeroForge random saved Hero page
# Open a new browser tab with a random saved HeroForge character
import random, webbrowser
# append the page number on the end of this address
pre_address = "https://www.heroforge.com/load_share%3D"
# the last page number (inclusive), page numbers start at 1
page_last = 511695067

random_page_number = random.choice(range(1, page_last + 1))
full_address = pre_address + str(random_page_number) + '/'
# print(full_address)
webbrowser.open(full_address, new=2)
# input("Press Enter to close.")
