#!/bin/bash

#do some stuff

apt-get install -y python-pip python-virtualenv libreadline-dev libconfig-dev libssl-dev lua5.2 liblua5.2-dev git libevent-dev make

sudo -u vagrant git clone https://github.com/efaisal/tg.git /home/vagrant/tg
cd /home/vagrant/tg
sudo -u vagrant ./configure && make
sudo -u vagrant virtualenv /home/vagrant/virtualenv

