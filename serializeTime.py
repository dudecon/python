from numbers import Real
import timeit
class process_template(object):
    def __init__(self):
        self.label = "blank"
        self.children = []
        self.duration_cached = 0
        self.start = 0
        self.end = 0
    def __str__(self):
        return self.label + ": lasts " + str(self.duration)
    def __repr__(self):
        return str(self)
    def serialTime(self):
        label = self.label
        startLabel = label + " starts"
        endLabel = label + " ends"
        serialData = [(startLabel,self.start),(endLabel,self.end)]
        for child in self.children:
            childSerial = child.serialTime()
            serialData += childSerial
        def srt(pair): return pair[1]
        serialData.sort(key=srt)
        self.cacheDuration()
        return serialData
    def calcDuration(self):
        return 0
    def cacheDuration(self):
        self.duration_cached = self.duration
    @property
    def duration(self):
        cached = self.duration_cached
        if cached is not None:
            return cached
        return self.calcDuration()
    
class atomicProcess(process_template):
    def __init__(self, label, duration):
        assert isinstance(label, str)
        self.label = label
        assert isinstance(duration, Real)
        self.duration_cached = duration
        self.children = []
        self.start = 0
        self.end = duration
        
class paralellProcess(process_template):
    def __init__(self, label, children):
        assert isinstance(label, str)
        self.label = label
        childList = []
        for child in children:
            assert isinstance(child, process_template)
            childList += [child]
        self.children = childList
        self.duration_cached = None
        self.start = 0
    @property
    def end(self):
        return self.start + self.duration
    def __getitem__(self, key):
        return self.children[key]
    def __setitem__(self, key, value):
        self.children[key] = value
    def __delitem__(self, key):
        del self.children[key]
    def calcDuration(self):
        duration = 0
        for child in self.children:
            duration = max(duration, child.duration)
        return duration
    
class sequentialProcess(paralellProcess):
    def calcDuration(self):
        duration = 0
        for child in self.children:
            duration += child.duration
        return duration
    def serialTime(self):
        label = self.label
        startLabel = label + " starts"
        endLabel = label + " ends"
        serialData = [(startLabel,0),(endLabel,self.duration)]
        currentTime = 0
        for child in self.children:
            childSerial = [(name, time + currentTime) for (name, time) in child.serialTime()]
            serialData += childSerial
            currentTime += child.duration
        def srt(pair): return pair[1]
        serialData.sort(key=srt)
        self.cacheDuration()
        return serialData

def multiProcess(label, lengths):
    components = []
    i = 0
    for curLength in lengths:
        i += 1
        curLabel = label + " " + str(i)
        curProc = atomicProcess(curLabel, curLength)
        components += [curProc]
    return components

# Test and example code

mainComponents = multiProcess("sub-process", [-3, 29, 0, 7])
mainProc = sequentialProcess("Main Process", mainComponents)

prerequComponents = multiProcess("Prerequisite", [2, 19, -20, 7])
prerequProc = paralellProcess("pre-work", prerequComponents)

followOnComponents = multiProcess("finish", [7,6,1])
followOnProcess = paralellProcess("cleanup", followOnComponents)

concurrentComponents = multiProcess("concur", [12,15,9])
concurrentProcess = sequentialProcess("main concurrent", concurrentComponents)

coreProc = paralellProcess("core", [mainProc, concurrentProcess])

fullProcess = sequentialProcess("full process", [prerequProc, coreProc, followOnProcess])

#print("full duration", timeit.timeit('fullProcess.duration', "from __main__ import fullProcess"))
serializedInfo = fullProcess.serialTime()
#print("serialized full process:", serializedInfo)
print(len(serializedInfo))
print("full duration, serialized", timeit.timeit('fullProcess.duration', "from __main__ import fullProcess"))
