import codecs
import random

eightball_choice = ['Vg vf pregnva',
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
    """ Registers up the 8ball plugin. """
    return {'regex': "^8.?ball.*\?", 'act_on_event': 'message', 'cooldown': 10}


def run(msg):
    """ Returns the answer to a yes/no question from the magic 8ball. """
    answer = codecs.decode((random.choice(eightball_choice)), 'rot13')
    return ({'action': 'send_msg', 'payload': answer},)
