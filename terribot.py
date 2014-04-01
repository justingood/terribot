#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A terrible Telegram bot. NOT Three-Law compatible.
"""

import sys
from datetime import datetime, timedelta
import pytg
from pytg.utils import coroutine, broadcast
from pytg.tg import (
    dialog_list, chat_info, message, user_status,
)

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
            print msg
            if msg['gid'] == chat_group:
                cmd = msg['message'].strip().split(' ')
                if len(cmd) == 1:
                    # ping command
                    if cmd[0].lower() == 'ping':
                        now = datetime.now()
                        # simple ping flood control
                        if not last_ping or (now - last_ping) >= mydelta:
                            last_ping = now
                            # Send pong respond to this chat group
                            tg.msg(msg['cmdgroup'], 'pong')
                    # quit command
                    elif cmd[0].lower() == 'quit':
                        if msg['uid'] == '17696710': # Put your user id here
                            tg.msg(msg['cmdgroup'], 'By your command')
                            QUIT = True
    except GeneratorExit:
        pass


if __name__ == '__main__':
    # Instantiate Telegram class
    telegram = os.getenv('TELEGRAM_BINARY')
    pubkey = os.getenv('TELEGRAM_PUBKEY')
    tg = pytg.Telegram(telegram, pubkey)

    # Create processing pipeline
    # Bot will respond to command the posted in this chat group
    whichgroup = os.getenv('TELEGRAM_ENV', 'DEVELOPMENT' )

    grpuid = os.getenv('TELEGRAM_ENV', 'DEVELOPMENT' )
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
