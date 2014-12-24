#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A terrible Telegram bot. NOT Three-Law compatible.
"""

import sys
import os
import time
from datetime import datetime, timedelta
import pytg
from pytg.utils import coroutine, broadcast
from pytg.tg import (
    dialog_list, chat_info, message, user_status,
)
import magic
from collections import deque
import ConfigParser

os.system("/usr/bin/killall telegram")

config = ConfigParser.RawConfigParser()
config.read('config.cfg')

twitter_disabled = False

deployment = os.getenv('DEPLOYMENT')
if deployment is None:
    deployment = 'development'

telegram_dir = config.get(deployment, 'telegram_dir')
bot_id = config.get(deployment, 'bot_id')
watch_rooms = config.get(deployment, 'watch_rooms')
try:
    twitter_token = config.get(deployment, 'twitter_token')
    twitter_token_key = config.get(deployment, 'twitter_token_key')
    twitter_consecret = config.get(deployment, 'twitter_consecret')
    twitter_consecretkey = config.get(deployment, 'twitter_consecretkey')
except:
    print "Couldn't load twitter."
    twitter_disabled = True

QUIT = False

last_def = None
last_wow = None
last_imgme = None

#Initialization. What's the worst that could happen?
lastMessage = deque([('XVYYNYYGURUHZNAF'.decode('rot13'))])

@coroutine
def command_parser(chat_group, tg):
    global QUIT
    last_ping = None
    # To avoid ping flood attack, we'll respond to ping once every 10 sec
    mydelta = timedelta(seconds=10)
    print "Ready and awaiting orders.\n\n"
    try:
        while True:
            msg = (yield)
            # Only process if the group name match
            print msg
            if msg['peer'] == "user":
                #don't crash
                print "getting result"
                result = magic.direct(msg)
                if botfunction == 'usr_msg':
                  tg.msg(msg['cmduser'], resultdata)

            elif msg['gid'] in watch_rooms and msg['uid'] != bot_id:
                result = magic.do(msg)
                #validate the result type and send it along it to the appropriate handler.
                # results will look like = [('a', 'A'), ('b', 'B')]
                for i, (botfunction, resultdata) in enumerate(result):
                    if botfunction == 'usr_msg':
                        pagingstring = msg['user'] + " paged you in the chat called " + msg['group']
                        tg.msg(resultdata, pagingstring)
                    if botfunction == 'msg':
                        tg.msg(msg['cmdgroup'], resultdata)
                    if botfunction == 'send_photo':
                        tg.send_photo(msg['cmdgroup'], resultdata)
                        time.sleep(0.2)
                        os.remove(resultdata)
                    if botfunction == 'send_video':
                        tg.send_video(msg['cmdgroup'], resultdata)
                    if botfunction == 'send_text':
                        tg.send_text(msg['cmdgroup'], resultdata)
                    print "The previous message was: %s" % lastMessage[0]
                    lastMessage.pop()
                    lastMessage.appendleft(msg['message'])
    except GeneratorExit:
        pass


if __name__ == '__main__':
    if telegram_dir is None:
        print "You must set the telegram_dir configuration option."
        sys.exit()
    else:
        telegram = telegram_dir.rstrip("/") + "/telegram"
        pubkey = telegram_dir.rstrip("/") + "/tg.pub"

    if bot_id is None:
        print "You need to set the bot_id configuration option."
        sys.exit()

    if watch_rooms is None:
        print "You need to set the watch_rooms configuration option."
        sys.exit()
    #This grpuid stuff has to change to wach_rooms list.
    else:
        grpuid = watch_rooms

    tg = pytg.Telegram(telegram, pubkey)
    pipeline = message(command_parser(grpuid, tg))

    # Register our processing pipeline
    tg.register_pipeline(pipeline)

    # Start telegram cli
    tg.start()
    try:
	while True:
            # Keep on polling so that messages will pass through our pipeline, but don't peg the CPU
	    time.sleep(0.001)
            tg.poll()

            if QUIT == True:
                break
    except KeyboardInterrupt:
        print "\nCuriously enough, the only thing that went through the mind of the bowl of petunias as it fell was Oh no, not again."
    # Quit gracefully
    tg.quit()
