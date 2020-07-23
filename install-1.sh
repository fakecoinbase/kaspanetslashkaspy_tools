#!/bin/bash
#
# Use this script to prepare a clean ubuntu server to run kaspytools applications.
# The script ends phase 1 of the installation and reboots.
# After reboot run install-2.sh

red=$'\e[1;31m'
grn=$'\e[1;32m'
yel=$'\e[1;33m'
blu=$'\e[1;34m'
mag=$'\e[1;35m'
cyn=$'\e[1;36m'
end=$'\e[0m'

# Install python 3.8 with all prerequisites
printf "%s\n" "${grn}Installing python (3.8) globally.${end}"

sudo apt update
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt install python3.8 -y
sudo apt-get install python3.8-dev -y


# Install pip3
printf "%s\n" "${grn}Installing and upgrading pip3.${end}"
sudo apt install python3-pip -y

# Upgrade pip3
python3.8 -m pip install --upgrade pip

# install virtualenv
printf "%s\n" "${grn}Installing virtualenv.${end}"
sudo python3.8 -m pip install virtualenv

#install docker
printf "%s\n" "${grn}Installing docker.${end}"
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
printf "%s\n" "${grn}Configure permissions for docker.${end}"
sudo groupadd -f docker
sudo usermod -aG docker $USER
newgrp docker
printf "%s\n" "${grn}===>>> REBOOT <<<===${end}"
systemctl reboot
