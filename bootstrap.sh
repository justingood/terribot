#!/bin/bash

apt-get install -y python-pip python-virtualenv libreadline-dev libconfig-dev libssl-dev lua5.2 liblua5.2-dev git libevent-dev make
sudo -u vagrant git clone https://github.com/efaisal/tg.git /home/vagrant/tg
cd /home/vagrant/tg
sudo -u vagrant ./configure && make
sudo -u vagrant mkdir /home/vagrant/.telegram
sudo -u vagrant virtualenv /home/vagrant/virtualenv
sudo -u vagrant /home/vagrant/virtualenv/bin/pip install -r /vagrant/requirements.txt
echo "source /home/vagrant/virtualenv/bin/activate; cd /vagrant" > /home/vagrant/.bash_profile
