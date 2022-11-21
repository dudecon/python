# opens a random McMaster Carr catalog page
from random import choice
import webbrowser

# 3873 fetched on 2017-09-20
# 3939 fetched on 2018-11-29
# 4239 fetched on 2022-11-21
HIGHEST_PAGE_NUMBER = 4239
pre_address = "http://www.mcmaster.com/#catalog/128/"

try:
    f = open('mcm_page_numbers.txt','r')
    maxpgraw = f.readline()
    raw = f.readline()
    f.close()
    maxpg = int(maxpgraw)
    rem_pgs = eval(raw)
    if maxpg == HIGHEST_PAGE_NUMBER: pass
    elif maxpg > HIGHEST_PAGE_NUMBER:
        while len(rem_pgs)>0:
            if rem_pgs[-1] > HIGHEST_PAGE_NUMBER: rem_pgs.pop()
            else: break
    elif maxpg < HIGHEST_PAGE_NUMBER:
        for i in range(maxpg,HIGHEST_PAGE_NUMBER+1):
            rem_pgs.append(i)
    else: print("Something went terribly wrong")
except:
    rem_pgs = [i for i in range(1,HIGHEST_PAGE_NUMBER+1)]

inchoice = ""
print('Enter to bring up a McMaster page\n"s" to save, "sc" to save and close, "p" to print')
while len(rem_pgs) > 0:
    printflag = False
    if len(inchoice)!= 0:
        inchoice = inchoice.lower()
        initial = inchoice[0]
        if initial == 's':
            print("Saving")
            f = open('mcm_page_numbers.txt','w')
            f.write(str(HIGHEST_PAGE_NUMBER)+'\n')
            f.write(str(rem_pgs))
            f.close()
            if inchoice == 'sc': break
            inchoice = input('Saved :')
            
            continue
        elif initial == 'p':
            print(rem_pgs)
            inchoice = input('Those are the currently loaded indicies :')
            continue
    idx = choice(range(len(rem_pgs)))
    chosen_page = rem_pgs.pop(idx)
    webbrowser.open(f'{pre_address}{chosen_page}')
    inchoice = input('Page {} queued:'.format(chosen_page))
