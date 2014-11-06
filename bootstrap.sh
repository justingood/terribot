#!/bin/bash

apt-get install -y python-pip python-virtualenv libreadline-dev libconfig-dev libssl-dev lua5.2 liblua5.2-dev git libevent-dev make
sudo -u vagrant git clone https://github.com/efaisal/tg.git /home/vagrant/tg
cd /home/vagrant/tg
sudo -u vagrant ./configure && make
sudo -u vagrant mkdir /home/vagrant/.telegram
sudo -u vagrant virtualenv /home/vagrant/virtualenv
sudo -u vagrant /home/vagrant/virtualenv/bin/pip install -r /vagrant/requirements.txt
echo "source /home/vagrant/virtualenv/bin/activate; cd /vagrant" > /home/vagrant/.bash_profile

cat <<EOF > /etc/motd.tail


          Welcome to the Terribot dev environment!
          -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
This should get you up and running fairly quickly. Plus, if you muck it up, you can always tear it down and start again!

There's just a bit more required before you're ready to start. First, you need to set up your bot's account in the Telegram-CLI software.
Run the following:

/home/vagrant/tg/telegram -k /home/vagrant/tg/tg.pub

Once that's set up, you can type 'safe_quit' to exit. You may want to backup the 'auth' file it generates at /home/vagrant/.telegram/auth to avoid this process next time.

To start the bot, change to the terribot directory, copy ''config.cfg.sample'' to ''config.cfg'', change it to match the values you want and run the main python file:

cd /home/vagrant/telegram
python terribot.py



EOF
