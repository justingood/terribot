import codecs
import random

# These are possible responses obscured in ROT13
who_choice = ['Jub\'f guvf Pbyva crefba lbh thlf xrrc gnyxvat nobhg?',
              'Pbyva? Jub\'f gung?',
              'Jung\'f n Pbyva?',
              'Lbh thlf xrrc fnlvat gung anzr...',
              'V unir ab vqrn jub lbh\'er gnyxvat nobhg.',
              'Fgbc znxvat hc vzntvanel cbrcyr.',
              'Guvf Pbyva thl fbhaqf nf vzntvanel nf uhzna serr jvyy']

# We'll pad this with extra empty data so we only sporadically comment
while len(who_choice) < 50:
    who_choice.append('')

# The user this should act on
whoUser = "colin"
whoRegex = "^" + whoUser + ".*"


def setup():
    return {'regex': whoRegex, 'act_on_event': 'message', 'cooldown': 2}


def run(msg):
    string = codecs.decode((random.choice(who_choice)), 'rot13')
    if string == '':
        return ()
    else:
        return ({'action': 'send_msg', 'payload': string},)
