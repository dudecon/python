#Headline builder
#Based on an image by DOGHOUSEDIARIES
#programmed by Paul Spooner

# built out of sub-phrases
# Each sub-phrase is a dict
# "s" is the key for the string. This is the text itself
# "gs" is a gendered string. use format() to insert the proper words
# "g" is the gender, "male", "female", or "neuter"

# standard news

# the first section of the headline
Sec1 = []
Sec1 += [{"s":"See how this"}]
Sec1 += [{"s":"Watch as this"}]
Sec1 += [{"s":"You won't believe how this"}]
Sec1 += [{"s":"Witness how this miracle"}]
Sec1 += [{"s":"The real reason this"}]
Sec1 += [{"s":"You'll never guess how this"}]
Sec1 += [{"s":"Behold in amazement as this"}]
Sec1 += [{"s":"Watch in horror as this"}]

# The second section of the headline
Sec2 = []
Sec2 += [{"s":"cute cat", "g":"neuter"}]
Sec2 += [{"s":"dopey dog", "g":"neuter"}]
Sec2 += [{"s":"homeless man", "g":"male"}]
Sec2 += [{"s":"homeless woman", "g":"female"}]
Sec2 += [{"s":"boy in kindergarten", "g":"male"}]
Sec2 += [{"s":"girl in kindergarten", "g":"female"}]
Sec2 += [{"s":"invention", "g":"neuter"}]
Sec2 += [{"s":"engineering student", "g":"male"}]
Sec2 += [{"s":"engineering student", "g":"female"}]
Sec2 += [{"s":"retired man", "g":"male"}]
Sec2 += [{"s":"retired woman", "g":"female"}]
Sec2 += [{"s":"home video", "g":"neuter"}]
Sec2 += [{"s":"outrageous viral video", "g":"neuter"}]

# The third section of the headline
Sec3 = []
Sec3 += [{"s":"will make you cry."}]
Sec3 += [{"gs":"will make you adore {0}.", "male":"him", "female":"her", "neuter":"it"}]
Sec3 += [{"s":"changes everything you believe."}]
Sec3 += [{"gs":"isn't what {0} seems.", "male":"he", "female":"she", "neuter":"it"}]
Sec3 += [{"s":"does the impossible."}]
Sec3 += [{"s":"impresses a delegation of congressmen."}]
Sec3 += [{"s":"shares a brilliant idea."}]
Sec3 += [{"gs":"reveals {0} true nature.", "male":"his", "female":"her", "neuter":"its"}]
Sec3 += [{"s":"attacks an innocent bystander."}]


#Shamus' Escapist article titles
# the first section of the headline
#Sec1 = []
Sec1 += [{"s":"This"}]
Sec1 += [{"s":"Learn how one"}]
Sec1 += [{"s":"Learn how this"}]
Sec1 += [{"s":"You won't believe how this"}]
Sec1 += [{"s":"Read on in horror as this"}]

# The second section of the headline
#Sec2 = []
Sec2 += [{"s":"grumpy man", "g":"male"}]
Sec2 += [{"s":"grumpy old man", "g":"male"}]
Sec2 += [{"s":"college dropout", "g":"male"}]
Sec2 += [{"s":"internet pundit", "g":"male"}]
Sec2 += [{"s":"author", "g":"male"}]
Sec2 += [{"s":"author you've never heard of", "g":"male"}]
Sec2 += [{"s":"programmer", "g":"male"}]
Sec2 += [{"s":"genius programmer", "g":"male"}]
Sec2 += [{"s":"gamer", "g":"male"}]
Sec2 += [{"s":"jobless nobody", "g":"male"}]
Sec2 += [{"s":"slacker", "g":"male"}]
Sec2 += [{"s":"games journalist", "g":"male"}]

# The third section of the headline
#Sec3 = []
Sec3 += [{"s":"exposes industry secrets."}]
Sec3 += [{"s":"changes everything you believe."}]
Sec3 += [{"gs":"reveals {0} secret to internet fame.", "male":"his", "female":"her", "neuter":"its"}]
Sec3 += [{"gs":"transforms EA Games with {0} scathing criticism.", "male":"his", "female":"her", "neuter":"its"}]
Sec3 += [{"s":"rages impotently at the shortsightedness of modern game developers."}]
Sec3 += [{"s":"shares a brilliant idea."}]
Sec3 += [{"gs":"reveals {0} true nature.", "male":"his", "female":"her", "neuter":"its"}]
Sec3 += [{"s":"rambles for a couple pages."}]


#concatenate a random selection
from random import choice
from time import sleep

def compose_headline():
    parts = []
    for i in (Sec1, Sec2, Sec3):
        parts += [choice(i)]
    gender = parts[1]["g"]
    if "gs" in parts[2].keys():
        parts[2]["s"] = parts[2]["gs"].format(parts[2][gender])
    return " ".join([i["s"] for i in parts])
while True:
    print(compose_headline())
    sleep(0.75)
