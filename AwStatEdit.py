# Log File Purge Script
# For reducing the size of the AwStats log files
from os import listdir
dir_path = path.dirname(path.realpath(__file__))
chdir(dir_path)
workingdir = "/home/father/Documents/StatEdit/"
thesefiles = listdir(workingdir)
# thesefiles = ['awstats012011.peripheralarbor.com.txt']
# print(thesefiles)
for filename in thesefiles:
    f = open(workingdir+filename, "r")
    filedata = f.read()
    f.close()
    filelines = filedata.split('\n')
    initiallines = len(filelines)
    strt = ""
    strt1 = "# URL with 404 errors - Hits - Last URL referer"
    strt2 = "# URL with 404 errors - Hits - Last URL referrer"
    if strt1 in filelines:
        strt = strt1
    elif strt2 in filelines:
        strt = strt2
    if strt != "":
        end = "END_SIDER_404"
        stidx = filelines.index(strt) - 1
        edidx = filelines.index(end) + 1
        filelines = filelines[:stidx] + filelines[edidx:]
        print("URL spots ", stidx, edidx)
    strt = "# Host - Pages - Hits - Bandwidth - Last visit date - [Start date of last visit] - [Last page of last visit]"
    if strt in filelines:
        end = "END_VISITOR"
        stidx = filelines.index(strt) + 4 + 25
        edidx = filelines.index(end)
        filelines = filelines[:stidx] + filelines[edidx:]
        print("Visitor spots ", stidx, edidx)
    strt = "# External page referers - Pages - Hits"
    if strt in filelines:
        end = "END_PAGEREFS"
        stidx = filelines.index(strt) + 4 + 25
        edidx = filelines.index(end)
        filelines = filelines[:stidx] + filelines[edidx:]
        print("Pageref spots ", stidx, edidx)
    finallines = len(filelines)
    if initiallines > finallines:
        print(filename, "reduced from", initiallines, "to", finallines, "lines")
    outdata = '\n'.join(filelines)
    f = open(workingdir+filename, 'w')
    f.write(outdata)
    f.close()

