# Document parsing script
# count up the number of words of each type

from collections import OrderedDict

filein = 'ffts_ps.html'
#filein = "test.txt"
fileout = 'wordcount.txt'
#fileout = 'testproduct.txt'

#number of characters to compare for each word
comp_len = 5

#open the file and read it into memory as "data"
'''f = open(filein, 'r')
data = f.read()
f.close()'''
data = '''It’s late in 2010, and things are finally coming to a head with the bank. Now that I’ve been laid off, money has become tight again. We missed a mortgage payment, then another. And another. The money just isn’t there. There are no cutbacks we could make that would bring us anywhere near the mortgage payment.

This is strangely liberating. For the first time in ages we’re paying all the (other) bills on time. Our finances stabilize. We no longer have a dozen problems. We only have one problem, which is that our mortgage is in default.

Note that I don’t really have any good pictures in our library to tell this story, so I’ve decided to scatter around some images of a trip the family took to the Carnegie Science Center in July 2010. I’ve loved the science center since I was a kid. It’s like Six Flags for your brain.

Kafkaesque

My daughter Rachel is experiencing the cerebral delight of having oddly-shaped objects in a place where nobody is going to yell, “Don’t touch that!” If you can walk through this without waving your hands over the “handrails” then you are officially Too Old.
I’m plugging along at my writing and freelance work, making what I can. Heather does paintings now and again, and sometimes works as an assistant for an antiques appraiser.

In the meantime, I’m trying to reconcile with the bank, somehow. The bank sends us a bunch of paperwork from their “loss mitigation” department. (Or is it loss litigation? Honestly, I can never remember. I like how either one works, though.) I fill it out and send it back. They’re offering to re-negotiate the terms of the loan. Applying for this is a somewhat convoluted, multi-step process.

Generally, when you’re dealing with a mortgage in default you’ve got three basic things you can do. In order, from least destructive to most destructive:

Re-negotiate or re-finance the loan. You can mess around with the interest rate or payment terms of the loan to make it easier to handle. The bank might make less money in the long run, or they might make more money but wait a lot longer to get it. The deadbeats get only a modest black mark on their record. This isn’t a bad outcome.
Short sale. If the deadbeat owes more than the house is worth, have them sell the house and all proceeds go to the bank. The bank can usually get a much better price for the place this way than if they unload it at auction. The bank takes a modest loss and the deadbeat walks away with nothing. Not a bad outcome, although the deadbeat needs to be willing to work with the bank. If they dig in and fight to stay in the house, then this option isn’t available.
Foreclose. Boot out the deadbeats and sell the house. The deadbeats get a massive black mark on their record and basically can’t borrow any money for a long time. The bank unloads the house at auction and gets a fraction of the value. Everyone loses.

Esther is playing an analog version of the classic Snake Game. In this version you control the snake by turning a wheel.
I’m sure there are other options in different circumstances, but these are the major ones I know about. I’m trying to work with the bank and pursue option #1, but they don’t seem to have their act together. I have a lot of conversations like this one:


INTERIOR - SHAMUS' OFFICE - DAY

SHAMUS is sitting at his desk with the phone pinned between his ear and his shoulder while he shuffles through a handful of scary-looking official documents.


SHAMUS
On page three of the packet it says to provide paycheck stubs to document my income.
MAN ON PHONE
(Reciting from a long-memorized script in a hurried monotone.)
They use those numbers to determine your eligibility for participation.

SHAMUS
Yeah, see. I don’t have paycheck stubs. I earn ad revenue and payment for contract work. But that income is irregular, and the form doesn’t give me a way to report irregular income.
(Beat.)
So how do I fill this out? Do you want an average? Over what time period? Or should I fill out a different form?

MAN
For your income?

SHAMUS
Yes sir.

MAN
Well, you’ll need to show any paycheck stubs on the form to determine your eligibility for participation.

All of my conversations with them are like this. It’s baffling. I don’t want to over-report my income. (Or else we’ll end up with a re-negotiated loan that I still can’t pay.) I don’t want to under-report it. (Which would be dishonest.) All of the forms ask for simple answers to complex questions and asking for clarifications leads to circular conversations.

Even more hilariously, there’s some sort of expiration date on this paperwork. They send me some, I send it back. They send me more, I send it back. We talk on the phone and clarify things, but rather than fixing things on the phone right then, they need me to write the clarifications down and send them in. Then we cross the sixty day (I’m guessing) threshold and suddenly all the paperwork is rendered void. The next time they call me they act like I’m a band new case and ask if I would like apply for the loss mitigation program. Okay, fine. Then it all begins again.


Issac is messing with some sort of wind-tunnel / paper airplane exhibit.
This drags on for nine months. Eventually I start to feel like I’m taking advantage of their crippling bureaucratic ineptitude to get free housing. I really feel guilty doing this. I’m happy to do whatever I can to make this right. Whatever works best for them. But instead we’re sending papers back and forth. I try sending a single payment. They send it back. (When a bank is foreclosing it’s normal to refuse payments like this. I don’t quite get the mechanics of it, but I understand this is normal.)

After almost a year of this I come to my senses and Google around for a mortgage calculator. I run the numbers myself and see that re-negotiation is impossible. There’s a limit on how low you can get the payments by extending the terms of the loan. You can’t ever get your payments lower than a single month of interest on the debt. Since we’ve been stacking on interest for a year now, this number has even gone up slightly. It’s not that far from my regular mortgage payment at this point, which means this entire year-long game of phone tag of paper-filing has been in pursuit of a mortgage that’s still too much for me to handle. They should have realized this ages ago. They had the information to figure this out from the first round of paperwork.

Sigh.

I suppose if I wanted to be a jerk I could keep playing this game and live here for free, but that would be wrong. I made a promise to pay back this loan and I’m failing to meet that promise. The least I can do is not be a jackass about it.

By now it’s 2011 and I’m putting a lot of time into a new book. I don’t have a title yet. The whole thing sprang from a funny idea I had while playing World of Warcraft. What if someone brought you back from the dead, but due to some sort of mix-up you weren’t the person they intended to revive? At the outset I was aiming for a comedic book, perhaps something like my Shamus Plays series. But right from the outset I lost my grip on the tone. It’s been drifting further and further from comedy and becoming a lighthearted action-adventure. That’s not bad or anything, but I didn’t know this was something that could happen to an author.


Dear Science Center: LINCOLN LOGS ARE NOT SCIENCE. They are the opposite of science. They are a low-tech toy that mimmics a very low-tech building technique. Having Lincoln Logs at the science center is like having a horse at an auto show. The only way this qualifies as science is in the archaeological or historical sense. 

But I gotta hand it to Lincoln Logs as a product. The toy is a hundred years old, and in all that time they haven’t changed a bit: No glow-in-the-dark, no fancy colors, no gimmicky playsets, no crossovers, no cutting corners with plastic logs, no chasing trends. Wood logs, green roof slats, and that’s it. Even the packaging has been immutable for over half a century.
I try asking the bank what THEY would like to do about this mortgage business, but then I just get a canned response offering the different mitigation programs and asking me to pick one. They either don’t care or aren’t allowed to express a preference.

I figure if I was in their shoes, I’d want the deadbeat to sell the property rather than go to foreclosure. So now I’m aiming for option #2. It’s not exactly “everybody wins”, but more like, “Everybody stops losing”. It stems the tide of red ink and lets Heather and I find a place where we can live within our means.

It takes the bank a long time to wrap their head around this idea. I mean, it’s one of the things they suggested, but they act like they don’t know how it works. They tell me to put the house on the market, which is impossible because I don’t know what they want to ask for it. If the place was any further underwater I’d have to pay my property taxes in seashells. There’s no possible way we could ask for the balance I owe, so the bank needs to take some kind of loss, here. I have no idea how much. They are a massive super-conglomerate with access to some of the most detailed home sales data on the planet. I’m a dummy who has already demonstrated he’s inept at this and shouldn’t be trusted with financial transactions more complex than buying a combo meal. I should not be setting the price. In fact, I have no right to do so. I mean, by setting the price I’d implicitly be deciding how much money they would lose.

They seem to figure this out after a few more months of phone-tag and paperwork. We finally get the house on the market and they set a price. Their price strikes me as being… extremely optimistic, but whatever. They’re a mortgage institution. They have to know what they’re doing when it comes to property values.

Thus begins several more months of foolishness. Once or twice a week, the realtor calls and tells us someone wants to see the place. We run off and let them show the house. (It’s summer, so we often go for ice cream.) Aside from needing to keep the place a bit cleaner than we prefer and needing to bug out at random times, this part is painless but also a little depressing. Lots and lots of people look at the place, and nobody makes an offer. Not even a bad, insulting, worthless offer.


This is another flight exhibit that combines airfoil with blowing air to explain how airplanes work. The sign behind Rachel says Roll, Pitch, Yaw.
The bank continues to call once or twice a week while this is going on. I wouldn’t mind, but every single phone conversation with them must begin with a long preamble where I have to recite basically everything.

Ring!

Hi, this is Shamus Young.

Hello I’m [Guy] calling on behlf of [bank]. May I speak with Shawmoze Young?

This is he.

You understand this call can be recorded?

Yes.

And you understand this is an attempt to collect a debt?

Yes.

And you understand that anything said here can be used for that purpose?

YES.

Can I have your social security number?

Blah blah numbers blah number blah.

And I also have [information] on a Heather Young. Is this correct?

Yes.

And can you state the address of the property.

[I state the ENTIRE address, including zip code.] (Why are they asking me this? Under what circumstances would either of us not know this, and what would happen if we didn’t?)

And the number I have on file for you is [reads me the same dang number he just called] is that correct?

Yes.

And are there any other contact numbers where we can reach you?

(This is a trick question. If I mention my wife’s cell phone, they ask me to recite it. If I say no then THEY recite it and ask me if it’s still valid. If I say “no” they will always ask me about this number anyway, every time, forever and ever.)

And can you confirm that you are currently living in the property with the intent to sell?

Yes.

Okay Mr. Young… [finally gets on with the call itself.]

I wouldn’t mind, but after a year of this it really begins to grate. It’s such a stupid waste of time, and after pissing away a couple of minutes with the boilerplate stuff the call usually ends with:

Okay Mr. Young, did you receive the paperwork and workout package sent out on [last month]?

Yes. We filled it out and sent it back.

[Typing on computer.] Okay Mr. Young, I see we did receive that paperwork on [last week]. Do you have any questions for me today?

YES! WHY DID YOU CALL ME AND PISS AWAY OUR TIME TO ASK ME A QUESTION YOU ALREADY HAD THE ANSWER TO, YOU FUMBLING SADIST?!? No, thank you.

Man. I know I’m the one in the wrong here, but these guys are not doing themselves any favors.

There’s a story of a friend-of-a-friend who lost her house to the bank. They foreclosed, and she fought eviction. When they finally got her to move out she went around the house and bashed holes in the drywall. I understand that losing your house is a sad or traumatic thing, but deliberately destroying the property just to spite them? Makes me mad. Why would you lash out at the bank? You’re the one who failed to pay! They’re just trying to stop losing money. From reading around the interwebs, I gather this kind of thing is actually common these days.

Now that I’m in a similar position I can kind of get where some of the anger is coming from. It’s frustrating trying to deal with a smothering bureaucracy that doesn’t have clear goals, doesn’t communicate well, and is careless with both your time and theirs. I’d never deliberately inflict additional financial damage on them, but I do find myself feeling a lot less contrite.'''
#print(data[:50])

#clean out anything between brackets, replace with whitespace
print("removing newlines")
data = data.replace('\n',' ')
print("Removing tags")
curpos = 0
while True:
    #parse looking for keyphrase
    found_pos = data.find('<', curpos)
    #print(found_pos)
    #loop until end of file reached
    if found_pos == -1:
        break
    #parse looking for end keyphrase
    end_pos = data.find('>', found_pos)
    #print(end_pos)
    if end_pos == -1:
        print("no close tag found, abort")
        break
    
    # remove the whole tag, but not the tagged text
    # Do this to the whole dataset, since tags are likely to repeat
    cut_string = data[found_pos:end_pos+1]
    #print(cut_string)
    data = data.replace(cut_string, "")
    #data = data[:cut_start] + ' ' + data[cut_end:]
    curpos = found_pos + 1

print("Removing Punctuation!")
#remove all punctuation
for character in '''"”“'’‘,;:.·()!?-*–%''':
    data = data.replace(character, '')

#print(data)
word_count = {}
all_words = data.split()
full_len = len(all_words)
print(full_len, "words")
# count all the words
print("Counting the words")
for word in all_words:
    search_word = word
    #uniform case
    search_word = search_word.capitalize()
    #trim plurality and posession from longer words
    if len(search_word) > 3:
        search_word = search_word.rstrip("s'’‘")
    #trim long words
    if len(search_word) > comp_len:
        search_word = search_word[:comp_len]
    #if nothing is left, continue
    if search_word == '': continue
    #increment the word count
    if search_word in word_count.keys():
        word_count[search_word] += 1
    else:
        word_count[search_word] = 1

print(len(word_count), "unique")

#sort the counts
word_list = OrderedDict(sorted(word_count.items(), key=lambda t: t[1], reverse=True))

#print(word_list.items())

#print it nicely

output = "A total of {} words were parsed,\n".format(full_len)
output += "of which {} were identified as unique.\n".format(len(word_count))
output += "Only the initial {} characters were considered.\n\n".format(comp_len)
output += ("       qty :  {:<" + str(comp_len) + "}  : ppm\n\n").format("word")
for datapair in word_list.items():
    #print(datapair[1], " : ", datapair[0])
    fraction = (datapair[1] / full_len) * 1000000
    output += ("{:>10,} :  {:<" + str(comp_len) + "}  : {:.2f}\n").format(datapair[1], datapair[0], fraction)
    #output += " %\n"



#save the file out
f = open(fileout, 'w')
f.write(output)
f.close()

print("done!")
