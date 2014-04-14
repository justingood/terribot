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

QUIT = False
DEBUG = False

last_def = None

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
            if msg['gid'] == chat_group and msg['gid'] != botid:
                result = magic.do(msg)
                #validate the result type and send it along it to the appropriate handler
                if result[0] == 'msg':
                    tg.msg(msg['cmdgroup'], result[1])
                if result[0] == 'send_photo':
                    print "sendin da photo!"
                    print msg['cmdgroup'], result[1]
                    tg.send_photo(msg['cmdgroup'], result[1])
                    time.sleep(0.2)
                    os.remove(result[1])
                if result[0] == 'send_video':
                    tg.send_video(msg['cmdgroup'], result[1])
                if result[0] == 'send_text':
                    tg.send_text(msg['cmdgroup'], result[1])
                print "The previous message was: %s" % lastMessage[0]
                lastMessage.pop()
                lastMessage.appendleft(msg['message'])
    except GeneratorExit:
        pass


if __name__ == '__main__':
    if os.getenv('TELEGRAM_DIR') is None:
        print "You must set the TELEGRAM_DIR environment variable."
        sys.exit()
    else:
        telegram = os.getenv('TELEGRAM_DIR').rstrip("/") + "/telegram"
        pubkey = os.getenv('TELEGRAM_DIR').rstrip("/") + "/tg.pub"

    if os.getenv('TELEGRAM_BOTID') is None:
        print "You need to set the TELEGRAM_BOTID environment variable"
        sys.exit()
    else:
        botid = os.getenv('TELEGRAM_BOTID')

    if os.getenv('TELEGRAM_ROOM') is None:
        print "You need to set the TELEGRAM_ROOM environment variable"
        sys.exit()
    else:
        grpuid = os.getenv('TELEGRAM_ROOM')
        
    tg = pytg.Telegram(telegram, pubkey)
    pipeline = message(command_parser(grpuid, tg))

    # Register our processing pipeline
    tg.register_pipeline(pipeline)

    # Start telegram cli
    tg.start()
    try:
	while True:
            # Keep on polling so that messages will pass through our pipeline, but don't peg the CPU
	    time.sleep(0.0001)
            tg.poll()

            if QUIT == True:
                break
    except KeyboardInterrupt:
        print "\nCuriously enough, the only thing that went through the mind of the bowl of petunias as it fell was Oh no, not again."
    # Quit gracefully
    tg.quit()
