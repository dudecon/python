# MCM random catalog page
# Open a new browser tab with a random page of the McMaster-Carr catalog
import random, webbrowser
# append the page number on the end of this address
pre_address = "http://www.mcmaster.com/#catalog/121/"
# the last page number (inclusive), page numbers start at 1
page_last = 3847

random_page_number = random.choice(range(1, page_last + 1))
full_address = pre_address + str(random_page_number)
# print(full_address)
webbrowser.open(full_address, new=2)
# input("Press Enter to close.")
