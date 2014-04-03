#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A terrible Telegram bot. NOT Three-Law compatible.
"""

import sys
import re
import pytg
import urllib2
import random
import urbandict
import json, requests
from bs4 import BeautifulSoup

colinChoice = ['Who\'s this Colin person you guys keep talking about?', 'Colin? Who\'s that?', 'What\'s a Colin?', 'You guys keep saying that name...', 'I have no idea who you\'re talking about.', 'Stop making up imaginary poeple.', 'This Colin guy sounds as imaginary as human free will', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',]
pingChoice = ['I\'m getting tired of ponging', 'Stop it', 'pong', 'pong', 'pong', 'Do you find this amusing?', 'pong', 'Pong', 'Qbert', 'pong', 'Not right now, I\'ve got a headache.', 'pong', 'pong', 'pong', 'pong', 'pong', 'pong', 'pong']

from pytg.utils import coroutine, broadcast
from pytg.tg import (
    dialog_list, chat_info, message, user_status,
    )

def do(msg):
    print msg
    print ""
    # Ping
    if re.match('ping' ,msg['message']) is not None:
        return random.choice(pingChoice)
    # URL Title Lookup
    elif re.search("(?P<url>https?://[^\s]+)", msg['message']) is not None:
        match = re.search("(?P<url>https?://[^\s]+)", msg['message'])
        soup = BeautifulSoup(urllib2.urlopen(match.group("url").replace(",","")))
        titlestring = soup.title.string.encode('utf-8', 'ignore')
        if re.search(" - YouTube", titlestring) is not None:
            return titlestring.replace(" - YouTube","")
        else:
            return titlestring
    # Cat facts
    elif re.search('(catfax)|(cat.?facts)', msg['message'], re.IGNORECASE) is not None:
        return json.loads((requests.get(url='http://catfacts-api.appspot.com/api/facts')).content.decode("utf-8"))["facts"][0]
    # Not cat facts
    elif re.search('facts', msg['message'], re.IGNORECASE) is not None and len(msg['message'].split()) == 2:
        return str(msg['message'] + "? " + "I can't give you those, unfortunately.")
    # Colin
    elif re.search('colin' ,msg['message'], re.IGNORECASE) is not None:
        return random.choice(colinChoice)
    elif re.search('define:' ,msg['message'], re.IGNORECASE) is not None and len(msg['message'].split()) >1:
        return str(urbandict.main("--define" + msg['message'].replace("define: ","")))
    # Ignore everything else
    else:
        return ''
