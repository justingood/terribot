terribot
========

A terrible Telegram chat robot.

**Reqirements**
You should probably have the following set up, to make development easy:
* [Virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/)
* [PyTG](https://github.com/efaisal/pytg) - The pytg directory should be copied into lib/python2.7/site-packages/ in your virtualenv
* [tg](https://github.com/efaisal/tg)


Also, some Local Environment variables - at a minimum:
* TELEGRAM_BINARY - *path to the tg CLI client*
* TELEGRAM_PUBKEY - *path the to tg CLI public key*
* TELEGRAM_ROOM - *group id of the room to be watched*
