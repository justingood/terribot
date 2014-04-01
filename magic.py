#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A terrible Telegram bot. NOT Three-Law compatible.
"""

import sys
import re
import pytg
import urllib2

from pytg.utils import coroutine, broadcast
from pytg.tg import (
    dialog_list, chat_info, message, user_status,
    )

def do(msg):
  print msg
  print ""
  if re.match('ping' ,msg['message']) is not None:
    return 'pong'
  elif re.search('http' ,msg['message']) is not None:
      from bs4 import BeautifulSoup
      soup = BeautifulSoup(urllib2.urlopen(msg['message']))
      return soup.title.string
  else:
    return ''
