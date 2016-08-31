"""Get an answer from the Magic Eightball."""
"""NB: will not return an ambiguous reply."""

import codecs
import random


eightball_pattern = r'''(?ix)
^           # start of string
(8.?ball)   # command
\s+         # some white-space
(.*\?)      # question
\s*         # optional white-space
$           # end of string
'''


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
    """Register up the 8ball plugin."""
    return {'regex': eightball_pattern, 'act_on_event': 'message', 'cooldown': 10}


def run(msg):
    """Return the answer to a yes/no question from the magic 8ball."""
    answer = codecs.decode(random.choice(eightball_choice), 'rot13')
    return ({'action': 'send_msg', 'payload': answer},)
