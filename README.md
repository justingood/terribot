terribot 
========
[![Deployment status from dploy.io](https://dotjustin.dploy.io/badge/23779029942745/15143.png)](http://dploy.io)

A terrible Telegram chat robot.

#### Vagrant
This is the easiest way to develop. First, get [Vagrant](https://www.vagrantup.com/) installed on your local machine. You'll probably want [Virtualbox](https://www.virtualbox.org/) too. Some sort of git client is probably a good idea too.

Then, you'll need to fork the repo via GitHub, and then clone that version locally.
Go into the code directory on your machine, and issue a ```vagrant up```, and the base machine will be downloaded, and then bootstrapped. Take note of the ssh port.
After that, you'll want to SSH into the newly created machine using your favorite SSH client. The username will be 'vagrant' and the password is also 'vagrant'.
Once in, you'll want to set up the telegram-cli client by changing to the directory with ```cd /home/vagrant/tg```.
Then set up your bot by running the client program with ```./telegram -k tg.pub```. Follow the steps, and then issue a ```safe_quit``` to exit the client when that's done.
An '''auth''' file is generated into the ```/home/vagrant/.telegram``` directory. You may want to back this up, so you can use it if you want to start from scratch again. If not, you can follow through the initial steps again.

The code can be [edited](https://atom.io/) on your machine.
Since the directory is available inside VM at '''/vagrant''', you can test your changes by going to the terribot directory and running the program.
```cd /vagrant```
```python terribot.py```

Once you're happy with your changes, commit them, and create a pull request so that change can be merged into the live bot.
