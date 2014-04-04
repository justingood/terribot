#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A terrible Telegram bot. NOT Three-Law compatible.
"""

import sys
import terribot
import re
import pytg
import urllib2
import random
import json, requests
from bs4 import BeautifulSoup
from httplib2 import Http
from datetime import datetime, timedelta

colinChoice = ['Jub\'f guvf Pbyva crefba lbh thlf xrrc gnyxvat nobhg?', 'Pbyva? Jub\'f gung?', 'Jung\'f n Pbyva?', 'Lbh thlf xrrc fnlvat gung anzr...', 'V unir ab vqrn jub lbh\'er gnyxvat nobhg.', 'Fgbc znxvat hc vzntvanel cbrcyr.', 'Guvf Pbyva thl fbhaqf nf vzntvanel nf uhzna serr jvyy', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',]
pingChoice = ['V\'z trggvat gverq bs cbatvat', 'Fgbc vg', 'cbat', 'cbat', 'cbat', 'Qb lbh svaq guvf nzhfvat?', 'cbat', 'Cbat', 'Doreg', 'cbat', 'Abg evtug abj, V\'ir tbg n urnqnpur.', 'cbat', 'cbat', 'cbat', 'cbat', 'cbat', 'cbat', 'cbat']

from pytg.utils import coroutine, broadcast
from pytg.tg import (
    dialog_list, chat_info, message, user_status,
    )

def do(msg):
    print msg
    print ""
    #terribot.last_def = None  # THIS NEEDS TO MOVE TO THE PARENT. Otherwise it just gets reset every time, which is pointless.
    terribot.mydelta = timedelta(seconds=30)
    # Ping
    if re.match('ping' ,msg['message']) is not None:
        return (random.choice(pingChoice)).decode('rot13')
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
        return (random.choice(colinChoice)).decode('rot13')
    # Urban Dictionary definitions
    elif (re.search('define' ,msg['message'], re.IGNORECASE) is not None and len(msg['message'].split()) >1):  #if "define" is in the message AND message is more than one word.
        defkeyword = str(msg['message']).split(' ', 1)[0]
        if re.search('define', defkeyword, re.IGNORECASE):                                         #if define is the FIRST word, otherwise ignore it (so people can still use "define" in a sentence)
            now = datetime.now()
            if not terribot.last_def or (now - terribot.last_def) >= terribot.mydelta:
                terribot.last_def = now                                           
                h = Http()
                resp, rawcontent = h.request("http://api.urbandictionary.com/v0/define?term=%s" % urllib2.quote(msg['message'].replace(defkeyword,"")), "GET")   #send message to the API, without define keyword
                if re.search('no_results', rawcontent) is None:                     #if there is a definition for that word
                    rawcontent = rawcontent.replace("\\r", " ").replace("\\n", " ") #remove newline and carriage returns
                    content = json.loads(rawcontent)
                    for item in content['list'][0:1]:
                        definition = item['definition']                             #populate some variables
                        permalink = item['permalink']
                        word = item['word']
                        example = item['example']
                        if example:                                                 #if the definition also has an example then show it
                            return (word + ": " + definition + ".          " + "EXAMPLE: " + example).encode('utf-8', 'replace')
                        else:
                            return (word + ": " + definition).encode('utf-8', 'replace')
                else:
                    return "Sorry, but I couldn't find a definition for that word."
            else:
                return "Sorry, you'll have to wait ~10 seconds to look up another definition."
        else:
                return ''

    # Ignore everything else
    else:
        return ''
