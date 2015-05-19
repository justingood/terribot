#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A terrible Telegram bot. NOT Three-Law compatible.
"""

import sys
import os
import time
from datetime import timedelta
import magic
import configparser
import codecs
import json
from collections import deque
from pytg.sender import Sender
from pytg.receiver import Receiver
from pytg.utils import coroutine

config = configparser.RawConfigParser()
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
    print("Couldn't load twitter.")
    twitter_disabled = True

QUIT = False

last_def = None
last_wow = None
last_imgme = None

# Initialization. What's the worst that could happen?
lastMessage = deque(codecs.decode("XVYYNYYGURUHZNAF", "rot13"))


@coroutine
def command_parser(receiver):
    global QUIT
    last_ping = None
    # To avoid ping flood attack, we'll respond to ping once every 10 sec
    mydelta = timedelta(seconds=10)
    print("Ready and awaiting orders.\n\n")
    try:
        while True:
            msg = (yield)

            # DEBUG Telegram message output
            # print(json.dumps(msg, sort_keys=True, indent=4))
            # print("")

            # Telegram has its own paging service now.
            # if msg.peer.type == "user":
            #    print("getting result")
            #    result = magic.direct(msg)
            #    if botfunction == 'usr_msg':
            #        tg.msg(msg['cmduser'], resultdata)

            if not msg.own:
                result = magic.do(msg)
                # Validate the result type and send it along it to the
                # appropriate handler.
                # results will look like = [('a', 'A'), ('b', 'B')]
                for i, (botfunction, resultdata) in enumerate(result):
                    if botfunction == 'usr_msg':
                        pagingstring = msg['user'] + " paged you in the chat called " + msg['group']
                        tg.msg(resultdata, pagingstring)
                    if botfunction == 'msg':
                            # TODO: Probably shouldn't send a blank message
                            #  every time it doesn't match something...
                            sender.send_msg(msg['peer']['cmd'], resultdata)
                    if botfunction == 'send_photo':
                        sender.send_photo(msg['peer']['cmd'], resultdata)
                        time.sleep(0.2)
                        os.remove(resultdata)
                    print("The previous message was: %s" % lastMessage)
                    time.sleep(0.2)
                    lastMessage.pop()
                    lastMessage.appendleft(msg['text'])
    except GeneratorExit:
        pass


if __name__ == '__main__':
    if telegram_dir is None:
        print("You must set the telegram_dir configuration option.")
        sys.exit()
    else:
        telegram = telegram_dir.rstrip("/") + "/bin/telegram-cli"
        pubkey = telegram_dir.rstrip("/") + "/tg-server.pub"

    if bot_id is None:
        print("You need to set the bot_id configuration option.")
        sys.exit()

    if watch_rooms is None:
        print("You need to set the watch_rooms configuration option.")
        sys.exit()
    # This grpuid stuff has to change to watch_rooms list.
    else:
        grpuid = watch_rooms

    receiver = Receiver(host="localhost", port=4458)
    sender = Sender(host="localhost", port=4458)
    receiver.start()
    receiver.message(command_parser(receiver))

    # Quit gracefully
    receiver.stop()
