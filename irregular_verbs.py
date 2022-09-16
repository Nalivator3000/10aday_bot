import random

arise = ['arise', 'arose', 'arisen']
awake = ['awake', 'awoke', 'awoke']
be = ['be', 'was were', 'been']
bear = ['bear', 'bore', 'borne']
beat = ['beat', 'beat', 'beaten']
become = ['become', 'became', 'become']
begin = ['begin', 'began', 'begun']
bend = ['bend', 'bent', 'bent']
bet = ['bet', 'bet', 'bet']
bind = ['bind', 'bound', 'bound']
bite = ['bite', 'bit', 'bitten']
bleed = ['bleed', 'bled', 'bled']
blow = ['blow', 'blew', 'blown']
break_verb = ['break', 'broke', 'broken']
bring = ['bring', 'brought', 'brought']
build = ['build', 'built', 'built']
burst = ['burst', 'burst', 'burst']
buy = ['buy', 'bought', 'bought']
catch = ['catch', 'caught', 'caught']
choose = ['choose', 'chose', 'chosen']
come = ['come', 'came', 'come']
cost = ['cost', 'cost', 'cost']
creep = ['creep', 'crept', 'crept']
cut = ['cut', 'cut', 'cut']
deal = ['deal', 'dealt', 'dealt']
dig = ['dig', 'dug', 'dug']
dive = ['dive', 'dived', 'dived'] # or 'dove'
do = ['do', 'did', 'done']
draw = ['draw', 'drew', 'drawn']
dream = ['dream', 'dreamt', 'dreamt'] # or 'dreamed',  or 'dreamed
drink = ['drink', 'drank', 'drunk']
drive = ['drive', 'drove', 'driven']
eat = ['eat', 'ate', 'eaten']
fall = ['fall', 'fell', 'fallen']
feed = ['feed', 'fed', 'fed']
feel = ['feel', 'felt', 'felt']
fight = ['fight', 'fought', 'fought']
find = ['find', 'found', 'found']
fit = ['fit', 'fit', 'fit'] # or 'fitted', or 'fitted'
flee = ['flee', 'fled', 'fled']
fling = ['fling', 'flung', 'flung']
fly = ['fly', 'flew', 'flown']
forbid = ['forbid', 'forbade', 'forbidden']
forget = ['forget', 'forgot', 'forgotten'] # or 'forgot'
forgive = ['forgive', 'forgave', 'forgiven']
freeze = ['freeze', 'froze', 'frozen']
get = ['get', 'got', 'got'] # or 'gotten'
give = ['give', 'gave', 'given']
go = ['go', 'went', 'gone']
grow = ['grow', 'grew', 'grown']
hang = ['hang', 'hung', 'hung']
have = ['have', 'had', 'had']
hear = ['hear', 'heard', 'heard']
hide = ['hide', 'hid', 'hidden']
hit = ['hit', 'hit', 'hit']
hold = ['hold', 'held', 'held']
hurt = ['hurt', 'hurt', 'hurt']
keep = ['keep', 'kept', 'kept']
kneel = ['kneel', 'knelt', 'knelt']
knit = ['knit', 'knitted', 'knitted']
know = ['know', 'knew', 'known']
lay = ['lay', 'laid', 'laid']
lead = ['lead', 'led', 'led']
leave = ['leave', 'left', 'left']
lend = ['lend', 'lent', 'lent']
let = ['let', 'let', 'let']
lie = ['lie', 'lay', 'lain']
light = ['light', 'lit', 'lit']
lose = ['lose', 'lost', 'lost']
make = ['make', 'made', 'made']
mean = ['mean', 'meant', 'meant']
meet = ['meet', 'met', 'met']
pay = ['pay', 'paid', 'paid']
plead = ['plead', 'pleaded', 'pled']
prove = ['prove', 'proved', 'proved'] # or 'proven'
put = ['put', 'put', 'put']
quit_verb = ['quit', 'quit', 'quit']
read = ['read', 'read', 'read']
ride = ['ride', 'rode', 'ridden']
ring = ['ring', 'rang', 'rung']
rise = ['rise', 'rose', 'risen']
run = ['run', 'ran', 'run']
say = ['say', 'said', 'said']
see = ['see', 'saw', 'seen']
seek = ['seek', 'sought', 'sought']
sell = ['sell', 'sold', 'sold']
send = ['send', 'sent', 'sent']
sew = ['sew', 'sewed', 'sewn'] # or 'sewed'
shake = ['shake', 'shook', 'shaken']
shine = ['shine', 'shone', 'shone']
shoot = ['shoot', 'shot', 'shot']
show = ['show', 'showed', 'shown'] # or 'shown'
shrink = ['shrink', 'shrank', 'shrunk']
shut = ['shut', 'shut', 'shut']
sing = ['sing', 'sang', 'sung']
sink = ['sink', 'sank', 'sunk']
sit = ['sit', 'sat', 'sat']
slay = ['slay', 'slew', 'slain']
sleep = ['sleep', 'slept', 'slept']
slide = ['slide', 'slid', 'slid']
slit = ['slit', 'slit', 'slit']
speak = ['speak', 'spoke', 'spoken']
spend = ['spend', 'spent', 'spent']
spin = ['spin', 'spun', 'spun']
spit = ['spit', 'spat', 'spat'] # or spit, or spit
split = ['split', 'split', 'split']
spread = ['spread', 'spread', 'spread']
spring = ['spring', 'sprang', 'sprung']
stand = ['stand', 'stood', 'stood']
steal = ['steal', 'stole', 'stolen']
stick = ['stick', 'stuck', 'stuck']
sting = ['sting', 'stung', 'stung']
stink = ['stink', 'stank', 'stunk']
stride = ['stride', 'strode', 'stridden']
strike = ['strike', 'struck', 'struck']
string = ['string', 'strung', 'strung']
swear = ['swear', 'swore', 'sworn']
sweep = ['sweep', 'swept', 'swept']
swell = ['swell', 'swelled', 'swollen']
swim = ['swim', 'swam', 'swum']
swing = ['swing', 'swing', 'swung']
take = ['take', 'took', 'taken']
teach = ['teach', 'taught', 'taught']
tear = ['tear', 'tore', 'torn']
tell = ['tell', 'told', 'told']
think = ['think', 'thought', 'thought']
throw = ['throw', 'threw', 'thrown']
understand = ['understand', 'understood', 'understood']
wake_up = ['wake up', 'woke up', 'woken up'] # ro 'waked up'
wear = ['wear', 'wore', 'worn']
wed = ['wed', 'wed', 'wed']
weep = ['weep', 'wept', 'wept']
welcome = ['welcome', 'welcomed', 'welcomed']
wet = ['wet', 'wet', 'wet']
win = ['win', 'won', 'won']
wring = ['wring', 'wrung', 'wrung']
write = ['write', 'wrote', 'written']

dictionary = [arise, awake, be, bear, beat, become, begin, bend, bet, bind, bite, bleed, blow, bring, build, burst, buy,
             catch, choose, come, cost, creep, cut, deal, dig, dive, do, draw, dream, drink, drive, eat, fall, feed, feel,
             fight, find, fit, flee, fling, fly, forbid, forget, forgive, freeze, get, go, grow, hang, have, hear, hide,
             hit, hold, hurt, keep, kneel, knit, know, lay, lead, leave, lend, let, lie, light, lose, make, mean, meet,
             pay, plead, prove, put, read, ride, ring, rise, run, say, see, seek, sell, send, sew, shake, shine,
             shoot, show, shrink, shut, sing, sink, sit, slay, sleep, slide, slit, speak, spend, spin, spit, split, spread,
             spring, stand, steal, stick, sting, stink, stride, strike, string, swear, sweep, swell, swim, swing, take,
             teach, tear, tell, think, throw, understand, wake_up, wear, wed, weep, welcome, wet, win, wring, write,
             break_verb, quit_verb]

hard_mode = [bear, bind, dive, fling, knit, lie, plead, prove, sew, shrink, slay, slide, spin, spit, sting, stride, swell, swing, swim, tear, welcome, wring]

def get_mode():
    print('''
    1 - Random
    2 - Alphabet
    3 - My list''')
    mode = input('Choise a mode: ')
    mode = str('mode' + mode)
    if mode == 'mode1':
        mode1()
    elif mode == 'mode2':
        mode2()
    elif mode == 'mode3':
        mode3()
    else:
        return get_mode()
    
def mode1():
    next_word = list(dictionary[random.randint(0, len(dictionary) - 1)])
    p = random.randint(0, 1)
    form = next_word[p]
    if p == 0:
        word = input(f'Enter the second form of {next_word[0]}: ')
        if word == form:
            print('Excelent!')
            repeat_mode1()
        else:
            print('Correct is:')
            print(next_word)
            repeat_mode1()
    else:
        word = input(f'Enter the third form of {next_word[0]}: ')
        if word == form:
            print('Excelent!')
            repeat_mode1()
        else:
            print('Correct is:')
            print(next_word)
            repeat_mode1()

def mode3():
    next_word = list(hard_mode[random.randint(0, len(hard_mode) - 1)])
    p = random.randint(1, 2)
    form = next_word[p]
    if p == 1:
        word = input(f'Enter the second form of {next_word[0]}: ')
        if word == form:
            print('Excelent!')
            repeat_mode3()
        else:
            print('Correct is:')
            print(next_word)
            repeat_mode3()
    else:
        word = input(f'Enter the third form of {next_word[0]}: ')
        if word == form:
            print('Excelent!')
            repeat_mode3()
        else:
            print('Correct is:')
            print(next_word)
            repeat_mode3()
            
def repeat_mode1():
    print('To continue press Enter')
    print('"0" to main menu')
    repeat = input()
    if repeat == '':
        mode1()
    elif repeat == '0':
        get_mode()
    else:
        return repeat_mode1()

def repeat_mode3():
    print('To continue press Enter')
    print('"0" to main menu')
    repeat = input()
    if repeat == '':
        mode1()
    elif repeat == '0':
        get_mode()
    else:
        return repeat_mode3()
    
#get_mode()

