#!/bin/bash
#
# First run install-01.sh script,  to prepare a clean ubuntu server.
# The script ends by rebooting the machine.
# Then run this script.

# fill git usename and password (to get  automation_testing repository)
GITUSER=
GITPASS=

sudo curl -L "https://github.com/docker/compose/releases/download/1.26.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
mkdir kaspanet
cd kaspanet || exit

#create your virtual environment and activate it
virtualenv -p "$(which python3.8)" venv
source venv\bin\activate

# Clone repositories
git clone https://github.com/kaspanet/kaspy_tools
git clone https://github.com/kaspanet/kaspad
git clone https://github.com/kaspanet/kasparov
git clone https://"$GITUSER":"$GITPASS"@github.com/kaspanet/automation_testing


# install kaspy_tools dependencies
cd kaspy_tools || exit
pip install -r requirements.txt

# (optional) install automation_testing requirements
# First make sure graphviz compilation will pass
sudo apt-get install libgraphviz-dev -y
cd ~/kaspanet/automation_testing || exit
pip install -r requirements.txt

