#!/bin/bash
#
# First run install-01.sh script,  to prepare a clean ubuntu server.
# The script ends by rebooting the machine.
# Then run this script.

# fill git usename and password (to get  automation_testing repository)

red=$'\e[1;31m'
grn=$'\e[1;32m'
yel=$'\e[1;33m'
blu=$'\e[1;34m'
mag=$'\e[1;35m'
cyn=$'\e[1;36m'
end=$'\e[0m'

printf "%s\n" "${grn}Install docker-compose.${end}"
sudo curl -L "https://github.com/docker/compose/releases/download/1.26.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
printf "%s\n" "${grn}Create kaspanet directory.${end}"
mkdir kaspanet
cd kaspanet || exit

#create your virtual environment and activate it
printf "%s\n" "${grn}Create and activate virtualenv under kaspanet.${end}"
virtualenv -p "$(which python3.8)" venv
source venv\bin\activate

# Clone repositories
printf "%s\n" "${grn}Clone public repositories (without automation_testing).${end}"
git clone https://github.com/kaspanet/kaspy_tools
git clone https://github.com/kaspanet/kaspad
git clone https://github.com/kaspanet/kasparov


# install kaspy_tools dependencies
printf "%s\n" "${grn}Install kaspy_tools requirements.${end}"
cd kaspy_tools || exit
pip install -r requirements.txt

# (optional) install automation_testing requirements
# First make sure graphviz compilation will pass
sudo apt-get install libgraphviz-dev -y

printf "%s\n" "${red}$"
printf "To install automation_testing manually:"
printf "git clone git@github.com:kaspanet/automation_testing.git"
printf "or:"
printf "https://github.com/kaspanet/automation_testing.git"
printf "Then:"
printf "cd automation_testing"
printf "pip install -r requirements.txt"
printf "%s\n" "${end}"


