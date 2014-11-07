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

#### Vagrant
This way is easiest. First, get [Vagrant](https://www.vagrantup.com/) installed on your local machine. You'll probably want [Virtualbox](https://www.virtualbox.org/) too. Some sort of git client is probably a good idea too.

Then, roughly, you'll need to fork the repo, and then clone it.
Issue a ```vagrant up```, and the base machine will be downloaded, and then bootstrapped.
You'll want to set up the telegram-cli client by changing to the directory with ```cd /home/vagrant/tg```
Then set up your bot by running the client ```./telegram -k tg.pub```, and then issuing a ```safe_quit``` when that's done.
You may want to back up the '''auth''' file it generates, which you can use if you want to get up and going quickly again.

The code can be [edited](https://atom.io/) on your machine.
Since the directory is available inside VM at /vagrant, you can test your changes by going to the terribot directory and running the program.
```cd /vagrant```
```python terribot.py```

Once you're happy with your changes, commit them, and create a pull request so that change can be merged into the live bot.
