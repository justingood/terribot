terribot 
========
[![Deployment status from dploy.io](https://dotjustin.dploy.io/badge/23779029942745/15143.png)](http://dploy.io)

A terrible Telegram chat robot.

#### Vagrant
This is the easiest way to develop. First, get [Vagrant](https://www.vagrantup.com/) installed on your local machine. You'll probably want [Virtualbox](https://www.virtualbox.org/) too. Some sort of git client is probably a good idea too.

Then, roughly, you'll need to fork the repo, and then clone that version locally.
Issue a ```vagrant up```, and the base machine will be downloaded, and then bootstrapped.
You'll want to set up the telegram-cli client by changing to the directory with ```cd /home/vagrant/tg```
Then set up your bot by running the client ```./telegram -k tg.pub```, and then issuing a ```safe_quit``` when that's done.
You may want to back up the '''auth''' file it generates, which you can use if you want to get up and going quickly again.

The code can be [edited](https://atom.io/) on your machine.
Since the directory is available inside VM at /vagrant, you can test your changes by going to the terribot directory and running the program.
```cd /vagrant```
```python terribot.py```

Once you're happy with your changes, commit them, and create a pull request so that change can be merged into the live bot.
