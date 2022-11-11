# Mastermind like game

from random import choices, sample, shuffle
from time import sleep

DUPLICATES = False
HOWMANY    = True
WHICH      = False
NumGlyphs  = 36
SeqLen     = 3
Guesses    = 0

GLYPH_LIBRARY = '''0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿĀĂĄĆĈĊČĎĐĒĔĖĘĚĜĞĠĢĤĦĨĪĬĮİĲĴĶĸĺļľŀłńņňŊŌŎŐŒŔŖŘŚŜŞŠŢŤŦŨŪŬŮŰŲŴŶŸŹŻŽſƀƁƂƃƄƅƆƇƈƉƊƋƌƍƎƏƐƑƒƓƔƕƖƗƘƙƚƛƜƝƞƟƠơƢƣƤƥƦƧƨƩƪƫƬƭƮƯưƱƲƳƴƵƶƷƸƹƺƻƼƽƾƿǀǁǂǃǄǅǆǇǈǉǊǋǌǍǏǑǓǕǗǙǛǞǠǢǤǦǨǪǬǮǰǱǴǶǷǸǺǼǾȀȂȄȆȈȊȌȎȐȒȔȖȘȚȜȞȠȡȢȤȦȨȪȬȮȰȲȴȵȶȷȸȹȺȻȽȾȿɀɁɃɄɅɆɇɈɊɌɎɐɑɒɓɔɕɖɗɘəɚɛɜɝɞɟɠɡɢɣɤɥɦɧɨɩɪɫɬɭɮɯɰɱɲɳɴɵɶɷɸɹɺɻɼɽɾɿʀʁʂʃʄʅʆʇʈʉʊʋʌʍʎʏʐʑʒʓʔʕʖʗʘʙʚʛʜʝʞʟʠʡʢʣʤʥʦʧʨʩʪʫʬʭʮʯʰʱʲʳʴʵʶʷʸʹʺʻʼʽʾʿˀˁ˂˃˄˅ˆˇˈˉˊˋˌˍˎˏːˑ˒˓˔˕˖˗˘˙˚˛˝˞˟ˠˡˢˣˤˬ˭ˮ˯˰˱˲˳˴˵˶˷˸˹˺˻˼˽˾̵̅̆̌̍̎̏̐̑̾̿̀́͂̓̈́͊͋͌͛ͣͤͥͦͧͨͩͪͫͬͭͮͯ͜͟͢͝͞͠͡ͰͱͲͳʹ͵Ͷͷͺͻͼͽ;Ϳ΅Ά·ΈΉΊΏΐΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΤΥΦΧΨΩΪΫάέήίΰαβγδεζηθικλμνξοπρςστυφχψωϊϋόύώϏϐϑϒϓϔϕϖϗϘϚϜϞϠϢϤϥϦϧϨϪϬϮϰϱϲϳϴϵ϶ϷϸϹϺϻϼϽϾϿЀЁЂЃЄЅІЇЈЉЊЋЌЍЎЏАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯљњћќѝўџѠѡѢѣѤѥѦѧѨѩѪѫѬѭѮѯѰѱѲѳѴѵѶѷѸѹѺѻѼѽѾѿҀҁ҂҃҄҅҆҇҈҉ҊҌҎҐҒҔҖҘҚҜҞҠҢҤҦҨҪҬҮҰҲҴҶҸҺҼҾӀӁӃӅӇӉӋӍӐӒӔӖӘӚӜӞӠӢӤӦӨӪӬӮӰӲӴӶӸӺӼӾԀԂԄԆԈԊԌԎԐԒԔԖԘԚԜԞԠԢԤԨԪԬԮԲԳԴԵԶԷԸԹԺԻԼԽԾԿՀՁՂՃՄՅՆՇՈՉՊՋՌՍՎՏՐՑՒՓՔՕՖբգդեզէըթժիլխծկհձղճմյնշոչպջռսվտրցւփքօֆև६'''


def compute_glyphs(num_g, offset=0, randomize=False):
    end = min(len(GLYPH_LIBRARY),offset+num_g)
    if randomize:
        Shuffled = [i for i in GLYPH_LIBRARY]
        shuffle(Shuffled)
        GLYPHS = ''.join(Shuffled[offset:end])
    else: GLYPHS =  GLYPH_LIBRARY[offset:end]
    return GLYPHS


def choose_sequence(seq_len, glyphs):
    if DUPLICATES: seq = ''.join(choices(glyphs, k=seq_len))
    else:
        seq_len = min(seq_len,len(glyphs))
        seq = ''.join( sample(glyphs,   seq_len))
    return seq


def isvalidguess(seq, secret_sequence, glyphs, pr=False):
    seq_len = len(secret_sequence)
    numblyphs = len(glyphs)
    if (numblyphs <= 10) and seq.isnumeric():
        try:
            seq = ''.join([glyphs[int(i)] for i in seq])
            if pr: print(f'{seq} extracted from indicies')
        except: pass
    guess_len = len(seq)
    if guess_len != seq_len:
        print(f"your guess was {guess_len} glyphs long,\n\
but the sequence is {seq_len} long")
        return False
    for gl in seq:
        if gl not in glyphs:
            print(f"your guess contained {gl}\n\
which is not (currently) a valid glyph")
            return False
    return seq


def numcombos():
    options = NumGlyphs
    combos = NumGlyphs
    for i in range(SeqLen-1):
        if not DUPLICATES: options -= 1
        combos *= options
    return combos


helpstr = '''Type stuff to guess the secret sequence
# to show the glyph pool
% to toggle showing how many glyphs you guess are in the sequence
@ to toggle showing which glyphs you guess are in the sequence
! to disclose the sequence, and re-roll
+ to set the number of glyphs in the sequence, and re-roll
* to set the size of the glyph pool, and re-roll
^ to toggle duplicate glyphs, does NOT re-roll'''

print(helpstr)
allglyphs = compute_glyphs(NumGlyphs)
secret_sequence = choose_sequence(SeqLen,allglyphs)
lastguess = ''
cmd = '#'
while True:
    if len(cmd) == 0: print(helpstr)
    elif cmd[0] == '#':
        print('the current valid glyph set is as follows:')
        print(''.join(allglyphs))
        print(f'the secret sequence is {SeqLen} glyphs long')
    elif cmd[0] == '%':
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
    elif cmd[0] == '!':
        print(f'the secret sequence was {secret_sequence}')
        secret_sequence = choose_sequence(SeqLen,allglyphs)
    elif cmd[0] == '+':
        try:
            SeqLen = int(input("sequence should be how long? "))
            SeqLen = max(SeqLen, 1)
            secret_sequence = choose_sequence(SeqLen,allglyphs)
            SeqLen = len(secret_sequence)
            print(f"sequence is now\n{SeqLen} glyphs long")
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
                if option == 'L':
                    off = GLYPH_LIBRARY.find('A')
                    NumGlyphs = min(NumGlyphs, 26)
                    allglyphs = compute_glyphs(NumGlyphs, off)
                elif option == 'N':
                    off = 0
                    NumGlyphs = min(NumGlyphs, 36)
                    allglyphs = compute_glyphs(NumGlyphs, off)
                elif option == 'G':
                    off = GLYPH_LIBRARY.find('Α')
                    NumGlyphs = min(NumGlyphs, 23)
                    allglyphs = compute_glyphs(NumGlyphs, off)
                elif option == 'C':
                    off = GLYPH_LIBRARY.find('А')
                    NumGlyphs = min(NumGlyphs, 32)
                    allglyphs = compute_glyphs(NumGlyphs, off)
                elif option == 'A': # Armenian
                    off = GLYPH_LIBRARY.find('Բ')
                    NumGlyphs = min(NumGlyphs, 36)
                    allglyphs = compute_glyphs(NumGlyphs, off)
                elif option == 'R':
                    allglyphs = compute_glyphs(NumGlyphs, 0, True)
                else: allglyphs = compute_glyphs(NumGlyphs)
            else: allglyphs = compute_glyphs(NumGlyphs)
            NumGlyphs = len(allglyphs)
            secret_sequence = choose_sequence(SeqLen,allglyphs)
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
            if WHICH:
                corgl = ''
                for gl in lastguess:
                    if gl in secret_sequence: corgl += gl
                print(f'in your guess {corgl} are in the sequence')
                n = 0
                for i in range(len(secret_sequence)):
                    if secret_sequence[i] == lastguess[i]:
                        n += 1
                print(f'and {n} are in the correct location')
            elif HOWMANY:
                n = 0
                for gl in lastguess:
                    if gl in secret_sequence: n += 1
                print(f'{n} of your glyphs are in the sequence')
    else: print(helpstr)
    cmd = input('-> ')
