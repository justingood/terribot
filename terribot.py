#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A terrible Telegram bot. NOT Three-Law compatible.
"""

import sys
import os
from datetime import datetime, timedelta
import pytg
from pytg.utils import coroutine, broadcast
from pytg.tg import (
    dialog_list, chat_info, message, user_status,
)
import magic

QUIT = False

@coroutine
def command_parser(chat_group, tg):
    global QUIT
    last_ping = None
    # To avoid ping flood attack, we'll respond to ping once every 10 sec
    mydelta = timedelta(seconds=10)
    try:
        while True:
            msg = (yield)
            # Only process if the group name match
            #print msg
            if msg['gid'] == chat_group:
                magic.do(msg)

    except GeneratorExit:
        pass


if __name__ == '__main__':
    # Instantiate Telegram class
    telegram = os.getenv('TELEGRAM_BINARY')
    pubkey = os.getenv('TELEGRAM_PUBKEY')
    tg = pytg.Telegram(telegram, pubkey)

    # Create processing pipeline
    # Bot will respond to command the posted in this chat group
    whichenv = os.getenv('TELEGRAM_ENV', 'DEVELOPMENT' )
    if whichenv == 'PRODUCTION':
        grpuid = os.getenv('PRODROOM')
    elif whichenv == 'QA':
        grpuid = os.getenv('QAROOM')
    else:
        grpuid = os.getenv('DEVROOM')
    pipeline = message(command_parser(grpuid, tg))

    # Register our processing pipeline
    tg.register_pipeline(pipeline)

    # Start telegram cli
    tg.start()
    while True:
        # Keep on polling so that messages will pass through our pipeline
        tg.poll()

        if QUIT == True:
            break

    # Quit gracefully
    tg.quit()
