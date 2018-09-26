#!/bin/bash

# this script:
# - expects that yum is upgraded & updated
#    -> python is installed
# - selenium and all its dependencies
# first argument is USER under which selenium will be executed and desktop env is running

USER=""

var=$1
if [ ! -z ${var+x} ]; then USER=${var}; echo "USER is set to '${USER}'"; fi

# Install virtualenv, libcurl-devel, gcc, wget, unzipx
yum install python python-virtualenv wget unzip libcurl-devel unzip gcc openssl-devel bzip2-devel -y
# because of installation of python version 3.6
yum install https://centos7.iuscommunity.org/ius-release.rpm -y
yum install python36u python36u-pip python36u-devel -y

# Setup virtual environment
#virtualenv .virtenv
virtualenv --python=/usr/bin/python3.6 .virtenv
source .virtenv/bin/activate

# Install base requirements
pip3.6 install --upgrade setuptools
pip3.6 install selenium chromedriver ipython pycurl xlrd PyUserInput lxml
pip3.6 install configparser
pip3.6 install -U pip

export PATH=${PATH}:./
# Install Chromdriver - PATH must include "."

if ls geckodriver-v0.20.1-linux32.tar.gz 1> /dev/null 2>&1; then
echo "firefox-59.0.tar.bz2 exists"
else
wget https://github.com/mozilla/geckodriver/releases/download/v0.20.1/geckodriver-v0.20.1-linux32.tar.gz
tar -xvzf geckodriver-v0.20.1-linux32.tar.gz
fi
#cd /opt
if ls firefox-59.0.tar.bz2 1> /dev/null 2>&1; then
echo "firefox-59.0.tar.bz2 exists"
else
wget https://download-installer.cdn.mozilla.net/pub/firefox/releases/59.0/linux-x86_64/en-US/firefox-59.0.tar.bz2
tar xfj firefox-59.0.tar.bz2
fi

chown -R ${USER}:${USER} ./

echo -e "\nSetup Complete."

#
