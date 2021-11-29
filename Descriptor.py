#some experiments with sentence structure
class thingy:
    # a thing with some properties
    # the properties are auto-generated from "attr"
    attr = ["strong", "powerful"]
    def __init__(self, name="nemo"):
        self.name = str(name)
        for val in self.attr:
            exec("self.{0} = 0".format(val))
    def describe(self, other):
        print(self.name + " has nothing to say.")

class character(thingy):
    # something that is able to describe other things
    # characters can be "good" as well
    attr = thingy.attr + ["good"]
    def __init__(self, *args, **kwargs):
        thingy.__init__(self, *args, **kwargs)
        # auto-populate the vocabulary
        # each attribute has a list of "high, medium, low" terms
        self.vocabulary = {}
        for val in self.attr:
            # for now, just use these generic terms
            self.vocabulary[val] = ["very " + val, val, "not " + val]
    def describe(self, other):
        #print a description of the other thing
        print(self.name + " describes " + other.name + " as")
        #go through each attribute and print a description for it
        for val in self.attr:
            # if the other object doesn't have this attribute, skip it
            if val not in other.attr: continue
            #use relative values
            rel = eval("other.{0} - self.{0}".format(val))
            # is the relative value high, average, or low?
            if rel > 2: idx = 0
            elif rel < -1: idx = 2
            else: idx = 1
            # print out the description
            print(self.vocabulary[val][idx] + " (" + val + "="+ str(rel) + ")")

bob = character("bob")
bob.powerful = 5
bob.strong = 4
bob.vocabulary["good"][0] = "totally sweet"
nick = character("nick")
nick.good = 5
nick.vocabulary["powerful"] = ["way powerful", "decent", "lame"]
chair = thingy("chair")
chair.strong = 7

bob.describe(nick)
nick.describe(chair)
