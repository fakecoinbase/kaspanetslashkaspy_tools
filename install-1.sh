#!/bin/bash
#
# Use this script to prepare a clean ubuntu server to run kaspytools applications.
# The script ends phase 1 of the installation and reboots.
# After reboot run install-2.sh

# Install python 3.8 with all prerequisites
sudo apt update
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt install python3.8 -y
sudo apt-get install python3.8-dev -y

# Install pip3
sudo apt install python3-pip -y

# Upgrade pip3
python3.8 -m pip install --upgrade pip

# install virtualenv
sudo python3.8 -m pip install virtualenv

#install docker
sudo apt-get update
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common -y

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"  -y

sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io -y

# Configure permissions for docker
sudo groupadd -f docker
sudo usermod -aG docker $USER
newgrp docker
systemctl reboot