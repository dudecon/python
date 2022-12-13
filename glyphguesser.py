# Mastermind like game

from random import choices, sample, shuffle
from time import sleep

DUPLICATES = False
HOWMANY    = True
WHICH      = False
WHERE      = False
NumGlyphs  = 36
SeqLen     = 3
Guesses    = 0

GLYPH_LIBRARY = '''0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿĀĂĄĆĈĊČĎĐĒĔĖĘĚĜĞĠĢĤĦĨĪĬĮİĲĴĶĸĺļľŀłńņňŊŌŎŐŒŔŖŘŚŜŞŠŢŤŦŨŪŬŮŰŲŴŶŸŹŻŽſƀƁƂƃƄƅƆƇƈƉƊƋƌƍƎƏƐƑƒƓƔƕƖƗƘƙƚƛƜƝƞƟƠơƢƣƤƥƦƧƨƩƪƫƬƭƮƯưƱƲƳƴƵƶƷƸƹƺƻƼƽƾƿǀǁǂǃǄǅǆǇǈǉǊǋǌǍǏǑǓǕǗǙǛǞǠǢǤǦǨǪǬǮǰǱǴǶǷǸǺǼǾȀȂȄȆȈȊȌȎȐȒȔȖȘȚȜȞȠȡȢȤȦȨȪȬȮȰȲȴȵȶȷȸȹȺȻȽȾȿɀɁɃɄɅɆɇɈɊɌɎɐɑɒɓɔɕɖɗɘəɚɛɜɝɞɟɠɡɢɣɤɥɦɧɨɩɪɫɬɭɮɯɰɱɲɳɴɵɶɷɸɹɺɻɼɽɾɿʀʁʂʃʄʅʆʇʈʉʊʋʌʍʎʏʐʑʒʓʔʕʖʗʘʙʚʛʜʝʞʟʠʡʢʣʤʥʦʧʨʩʪʫʬʭʮʯʰʱʲʳʴʵʶʷʸʹʺʻʼʽʾʿˀˁ˂˃˄˅ˆˇˈˉˊˋˌˍˎˏːˑ˒˓˔˕˖˗˘˙˚˛˝˞˟ˠˡˢˣˤˬ˭ˮ˯˰˱˲˳˴˵˶˷˸˹˺˻˼˽˾ͰͱͲͳʹ͵Ͷͷͺͻͼͽ;Ϳ΅Ά·ΈΉΊΏΐΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΤΥΦΧΨΩΪΫάέήίΰαβγδεζηθικλμνξοπρςστυφχψωϊϋόύώϏϐϑϒϓϔϕϖϗϘϚϜϞϠϢϤϥϦϧϨϪϬϮϰϱϲϳϴϵ϶ϷϸϹϺϻϼϽϾϿЀЁЂЃЄЅІЇЈЉЊЋЌЍЎЏАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯљњћќѝўџѠѡѢѣѤѥѦѧѨѩѪѫѬѭѮѯѰѱѲѳѴѵѶѷѸѹѺѻѼѽѾѿҀҁ҂҃҄҅҆҇҈҉ҊҌҎҐҒҔҖҘҚҜҞҠҢҤҦҨҪҬҮҰҲҴҶҸҺҼҾӀӁӃӅӇӉӋӍӐӒӔӖӘӚӜӞӠӢӤӦӨӪӬӮӰӲӴӶӸӺӼӾԀԂԄԆԈԊԌԎԐԒԔԖԘԚԜԞԠԢԤԨԪԬԮԲԳԴԵԶԷԸԹԺԻԼԽԾԿՀՁՂՃՄՅՆՇՈՉՊՋՌՍՎՏՐՑՒՓՔՕՖբգդեզէըթժիլխծկհձղճմյնշոչպջռսվտրցւփքօֆև६'''


def compute_glyphs(num_g, offset=0, randomize=False):
    end = min(len(GLYPH_LIBRARY),offset+num_g)
    if randomize:
        Shuffled = [it for it in GLYPH_LIBRARY]
        shuffle(Shuffled)
        GLYPHS = ''.join(Shuffled[offset:end])
    else: GLYPHS =  GLYPH_LIBRARY[offset:end]
    return GLYPHS


def choose_sequence(seq_len, glyphs):
    if DUPLICATES: newseq = ''.join(choices(glyphs, k=seq_len))
    else:
        seq_len = min(seq_len,len(glyphs))
        newseq = ''.join( sample(glyphs,   seq_len))
    return newseq


def isnumericstr(instr):
    for g in instr:
        if g not in "0123456789": return False
    return True


def isvalidguess(seqtry, true_sequence, glyphs, pr=False):
    seq_len = len(true_sequence)
    numblyphs = len(glyphs)
    if (numblyphs <= 10) and isnumericstr(seqtry) and not isnumericstr(glyphs):
        try:
            seqtry = ''.join([glyphs[int(it)] for it in seqtry])
            if pr: print(f'   {seqtry} extracted from indicies')
        except: pass
    badglyph = False
    for glph in seqtry:
        if glph not in glyphs:
            print(f"   {glph} is not (currently) a valid glyph")
            badglyph = True
    if badglyph: return False
    guess_len = len(seqtry)
    if guess_len != seq_len:
        if guess_len == 1:
            seqtry = ''.join([seqtry,]*seq_len)
        else:
            print(f"your guess was {guess_len} glyphs long,\n\
but the sequence is {seq_len} long")
            return False
    return seqtry


def numcombos():
    options = NumGlyphs
    combos = NumGlyphs
    for notused in range(SeqLen-1):
        if not DUPLICATES: options -= 1
        combos *= options
    return combos


helpstr = '''Type stuff to guess the secret sequence
% to show the glyph pool
# to toggle showing how many glyphs you guess are in the sequence
@ to toggle showing which glyphs you guess are in the sequence
$ to toggle showing correct glyphs in the correct locations
! to disclose the sequence, and re-roll
+ to set the number of glyphs in the sequence, and re-roll
* to set the size of the glyph pool, and re-roll
^ to toggle duplicate glyphs, does NOT re-roll
& to set to Wordle-like rules (but with nonsense words)'''

print(helpstr)
allglyphs = compute_glyphs(NumGlyphs)
secret_sequence = choose_sequence(SeqLen,allglyphs)
lastguess = ''
cmd = '%'
while True:
    if len(cmd) == 0: print(helpstr)
    elif cmd[0] == '%':
        print('the current valid glyph set is as follows:')
        print(''.join(allglyphs))
        print(f'the secret sequence is {SeqLen} glyphs long')
    elif cmd[0] == '#':
        if HOWMANY:
            HOWMANY = False
            print('number of correct glyphs now hidden')
        else:
            HOWMANY = True
            print('number of correct glyphs now shown')
    elif cmd[0] == '@':
        if WHICH:
            WHICH = False
            print('correct glyphs now hidden')
        else:
            WHICH = True
            print('correct glyphs now shown')
    elif cmd[0] == '$':
        if WHERE:
            WHERE = False
            print('correct glyph positions now hidden')
        else:
            WHERE = True
            print('correct glyph positions now shown')
    elif cmd[0] == '&':
        DUPLICATES = True
        WHERE = True
        WHICH = True
        SeqLen = 5
        off = GLYPH_LIBRARY.find('A')
        NumGlyphs = 26
        allglyphs = compute_glyphs(NumGlyphs, off)
        NumGlyphs = len(allglyphs)
        secret_sequence = choose_sequence(SeqLen, allglyphs)
        SeqLen = len(secret_sequence)
        print(f"there are now {NumGlyphs} glyphs:")
        print(allglyphs)
        print(f"the sequence is {SeqLen} glyphs long.")
        print("correct glyph count and location display has been enabled")
        print("also, there may be duplicate glyphs in the sequence")
        Guesses = 0
    elif cmd[0] == '!':
        print(f'the secret sequence was {secret_sequence}')
        secret_sequence = choose_sequence(SeqLen,allglyphs)
        Guesses = 0
    elif cmd[0] == '+':
        try:
            SeqLen = int(input("sequence should be how long? "))
            SeqLen = max(SeqLen, 1)
            secret_sequence = choose_sequence(SeqLen,allglyphs)
            SeqLen = len(secret_sequence)
            print(f"sequence is now\n{SeqLen} glyphs long")
            Guesses = 0
        except:
            print(f"errorǃ sequence is still\n{SeqLen} glyphs long")
    elif cmd[0] == '*':
        print("how many glyphs? ")
        print('follow by a space to select options below')
        print('L to use just the Latin alphabet')
        print('N to use just the alpha-numeric (default)')
        print('G to use the Greek alphabet')
        print('A to use the Armenian alphabet')        
        print('C to use the Cyrillic alphabet')
        print('R to use a random set of glyphs')
        try:
            selection = input("-> ").split()
            NumGlyphs = int(selection[0])
            NumGlyphs = max(NumGlyphs, 2)
            if len(selection) > 1:
                option = selection[1][0].upper()
                if option == 'L': # Latin
                    off = GLYPH_LIBRARY.find('A')
                    NumGlyphs = min(NumGlyphs, 26)
                    allglyphs = compute_glyphs(NumGlyphs, off)
                elif option == 'N': # alpha-numeric
                    off = 0
                    NumGlyphs = min(NumGlyphs, 36)
                    allglyphs = compute_glyphs(NumGlyphs, off)
                elif option == 'G': # Greek
                    off = GLYPH_LIBRARY.find('Α')
                    NumGlyphs = min(NumGlyphs, 23)
                    allglyphs = compute_glyphs(NumGlyphs, off)
                elif option == 'C': # Cyrillic
                    off = GLYPH_LIBRARY.find('А')
                    NumGlyphs = min(NumGlyphs, 32)
                    allglyphs = compute_glyphs(NumGlyphs, off)
                elif option == 'A': # Armenian
                    off = GLYPH_LIBRARY.find('Բ')
                    NumGlyphs = min(NumGlyphs, 36)
                    allglyphs = compute_glyphs(NumGlyphs, off)
                elif option == 'R': # Randomized
                    allglyphs = compute_glyphs(NumGlyphs, 0, True)
                else: allglyphs = compute_glyphs(NumGlyphs)
            else: allglyphs = compute_glyphs(NumGlyphs)
            NumGlyphs = len(allglyphs)
            secret_sequence = choose_sequence(SeqLen,allglyphs)
            Guesses = 0
            SeqLen = len(secret_sequence)
            print(f"there are now {NumGlyphs} glyphs:")
            print(allglyphs)
        except:
            print(f"errorǃ there are still\n{NumGlyphs} glyphs")
    elif cmd[0] == '^':
        if DUPLICATES:
            DUPLICATES = False
            print('no duplicate glyphs allowed in the next sequence')
        else:
            DUPLICATES = True
            print('the next sequence may contain duplicate glyphs')
    elif isvalidguess(cmd, secret_sequence, allglyphs, False):
        seq = isvalidguess(cmd, secret_sequence, allglyphs, True)
        Guesses += 1
        if seq == secret_sequence:
            print(f"Yes! {seq} is correct! You win!")
            sleep(.5)
            bruteforce = numcombos()//2
            if Guesses < bruteforce/4: qual = "just "
            elif Guesses < bruteforce/2: qual = "only "
            else:                      qual = ''
            print(f"You guessed it in {qual}{Guesses} tries.")
            print(f"It would take about {bruteforce} to bruteforce it.")
            if Guesses < bruteforce/7:
                print('Take a moment to celebrate your victory!')
                sleep(1)
            print('Okay. New sequence generated.')
            secret_sequence = choose_sequence(SeqLen,allglyphs)
            sleep(.5)
            print('On with the game!')
            lastguess = ''
            Guesses = 0
        else:
            lastguess = seq
            if WHERE:
                goodpositions = '   '
                for i in range(len(secret_sequence)):
                    if secret_sequence[i] == lastguess[i]:
                        goodpositions += lastguess[i]
                    else: goodpositions += " "
                goodpositions += " are the correct glyphs in the correct locations"
                print(goodpositions)
            if WHICH:
                corgl = ''
                for gl in lastguess:
                    if gl in secret_sequence: corgl += gl
                if len(corgl):
                    if len(corgl)==1:
                        print(f'in your guess only {corgl} is in the sequence')
                    else: print(f'in your guess {corgl} are in the sequence')
                    n = 0
                    for i in range(len(secret_sequence)):
                        if secret_sequence[i] == lastguess[i]:
                            n += 1
                    if n: print(f'and {n} are in the correct location')
                else: print('none of those glyphs are in the sequence')
            elif HOWMANY:
                n = 0
                for gl in lastguess:
                    if gl in secret_sequence: n += 1
                print(f'{n} of your glyphs are in the sequence')
            elif not WHERE:
                print("that's not correct")
    else: print(helpstr)
    cmd = input('-> ')
