
# finds Fibonaci/Lucas like sequences which result in the queried number

def seed_search(seed,targ):
    window = [1,seed]
    while window[1] < targ:
        nex = window[0] + window[1]
        window.pop(0)
        window.append(nex)
    return window[1] == targ

def gen_sequence(seed, lngth = 23):
    window = [1, seed]
    sq = [0, 1, seed]
    for i in range(lngth):
        nex = window[0] + window[1]
        window.pop(0)
        window.append(nex)
        sq.append(nex)
    return sq

def find_seed(target):
    try:
        realtarget = int(target)
    except:
        print("please use a number next time")
        return 0
    if realtarget != target:
        print(f"please use an interger next time. Using {realtarget} instead.")
    if realtarget == 0:
        return 0
    if target < 0:
        realtarget *= -1
        print(f"please use a positive number next time. Using {realtarget} instead.")
    # now for the actual search
    curseed = 1
    while curseed != realtarget:
        if seed_search(curseed,realtarget): break
        curseed += 1
    return curseed

if __name__ == '__main__':
    import BaseConverter

    def convert_sequence(s,b):
        outlist = []
        BaseConverter.b(b)
        for i in s:
            outlist.append(BaseConverter.rebase(i))
        return ", ".join(outlist)

    found = set()
    for i in range(201):
        s = find_seed(i)
        if s in found:
            continue
        if i != s+1:
            print(f"lowest seed for {i} is {s}")
            found.add(s)
    for k in range(30):
        i = (1+k)*100
        s = find_seed(i)
        if i != s + 1:
            print(f"lowest seed for {i} is {s}")
    for i in (666,17):
        s = find_seed(i)
        print(f"lowest seed for {i} is {s}")
    for j in (1,3,4,5,6,7,8,17,666):
        sequence = gen_sequence(j)
        rebased = convert_sequence(sequence,j)
        print(f"the seed {j} produces {sequence}\nwhich in base {j} is {rebased}")