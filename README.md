terribot
========

A terrible Telegram chat robot.

**Reqirements**

You should probably have the following set up, to make development easy:
* [Virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/)
* [tg](https://github.com/efaisal/tg)


Also, some Local Environment variables - at a minimum:
* TELEGRAM_DIR - *path to the tg CLI client.*
* TELEGRAM_ROOM - *group id of the room to be watched*
* TELEGRAM_BOTID - *the UID of your bot. This is used so it avoids responding to its own messages, causing an infinite loop :-/*

**VirtualEnv**

Once you've got virtualenv installed, you can install all the required dependencies easily:
* Create virtualenv, if you haven't already <br>
```cd /path/to; virtualenv virtualenv```
* Activate your virtualenv <br>
```source /path/to/virtualenv/bin/activate```
* Install required python modules <br>
```cd /path/to/source; pip install -r requirements.txt```
