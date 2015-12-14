import codecs
import random

eightBallChoice = ['Vg vf pregnva',
                   'Vg vf qrpvqrqyl fb',
                   'Jvgubhg n qbhog',
                   'Lrf qrsvavgryl',
                   'Lbh znl eryl ba vg',
                   'Nf V frr vg, lrf',
                   'Zbfg yvxryl',
                   'Bhgybbx tbbq',
                   'Lrf',
                   'Fvtaf cbvag gb lrf',
                   'Qba\'g pbhag ba vg',
                   'Zl ercyl vf ab',
                   'Zl fbheprf fnl ab',
                   'Bhgybbx abg fb tbbq',
                   'Irel qbhogshy']


def setup():
    return {'regex': "^8.?ball.*\?", 'act_on_event': 'message'}


def run(msg):
    answer = codecs.decode((random.choice(eightBallChoice)), 'rot13')
    return ({'action': 'send_msg', 'payload': answer},)
