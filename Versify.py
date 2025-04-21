pretext = "\n[Instrumental]\n\n"
postext = "\n[Chorus]\n[Instrumental]\n\n[End]\n\n"

verses = """[Verse]
But you, man of God,
avoid all this. Instead,
pursue righteousness, devotion, faith,
love, patience, and gentleness.  
[Verse]
Compete well for the faith.
Lay hold of eternal life,
to which you were called
when you made the noble confession
in the presence of many witnesses.  
[Verse]
I charge [you] before God,
who gives life to all things,
and before Christ Jesus,
who gave testimony under Pontius Pilate
for the noble confession,  
[Verse]
to keep the commandment
without stain or reproach
until the appearance
of our Lord Jesus Christ
that the blessed and only ruler  
[Verse]
will make manifest at the proper time,
the King of kings
and Lord of lords,
who alone has immortality,
who dwells in unapproachable light,  
[Verse]
and whom no human being
has seen or can see.
To him be honor
and eternal power. Amen.  
[Verse]
Right Use of Wealth.
Tell the rich in the present age
not to be proud
and not to rely
on so uncertain a thing as wealth  
[Verse]
but rather on God,
who richly provides us
with all things for our enjoyment.
Tell them to do good,
to be rich in good works,  
[Verse]
to be generous, ready to share,
thus accumulating as treasure
a good foundation for the future,
so as to win the life
that is true life.  
[Verse]
O Timothy, guard what
has been entrusted to you.
Avoid profane babbling
and the absurdities
of so-called knowledge.  
[Verse]
By professing it, some people
have deviated from the faith.
Grace be with all of you.
"""
verses = verses.replace("\n\n","\n")
verses = verses.replace("\n\n","\n")
verses = verses.replace("\n\n","\n")
verses = verses.replace(" \n","\n")
verses = verses.replace(" \n","\n")
verses = verses.replace(" \n","\n")

verses = verses.replace("\n[Verse]\n","\n\n[Verse]\n")
print(pretext + verses + postext)
