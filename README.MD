
# KASPY_TOOLS

A set of tools that makes it easier to run and use kaspanet tools (kaspad, kasparov).

* [Getting Started](#getting-started)
  * [Getting the required tools](#getting-tools)
    * [Python and PIP](#python-pip)
    * [virtualenv](#virtualenv)
    * [docker and docker-compose](#docker-and-compose)
  * [Directory Structure](#directory-structure)
  * [Install Dependencies](#instal-dependencies)
  * [set environment variables](#environment-variables)
  * [Prepare Local configuration files](#local-conf-files)
    * [kaspy_tools_constants.py](#kaspy-tools-constants)
    * [docker-compose.yaml](#docker-compose)
* Current tools and utilities:
  * [Running locally](#local_run)
    * [Build kaspad](#build-kasoad)
    * [Build kasparov](#build-kasparov)
    * [Run Services](#run-services)
  * [JSON-RPC communication with kaspad](#JSON-RPC) (used with other tools)
  * [Kaspanet addresses](#kaspanet_addresses)
    * create private and public keys
    * create kaspanet addresses (Bech32 encoded) addresses.
  * Blocks
    * Creating and submitting a block based on a template from kaspad
    * Parsing a block given in binary form
  * Create complete DAGs
    * 
    * create small to medium  devnet DAGs (thousands of blocks)
    * create large DAGs (millions of blocks) based on simnet using a 
      pair of dedicatde "builder" kaspad containers.
      These containers use the simnet network and addresses, so they can 
      build DAGs very fast.
  * Transactions
    * Create transactions based on UTXOs in previous blocks.


  
  
### <a name="getting-started">Getting Started</a> 

#### <a name="getting-tools"> Getting the required tools </a>
##### <a name="python-pip"> Python and PIP </a>

Current kaspy_tools requires python version 3.8.0 and on.<br>
(Do not try to remove the version pre-installed on your system!!!)<br> 
Here are the required commands to install python3.8: <br>
(based on [this](https://linuxize.com/post/how-to-install-python-3-8-on-ubuntu-18-04/) article)
<pre>
`sudo apt update`
`sudo apt install software-properties-common`
`sudo add-apt-repository ppa:deadsnakes/ppa`
     (press ENTER to confirm)
`sudo apt install python3.8` <br>
</pre>

Make sure you also have pip3 installed:<br>
`sudo apt install python3-pip`<br>

Then upgreade pip:<br>
`python3.8 -m pip install --upgrade pip`<br>

Verify:
`python3.8 -m pip --version`

##### <a name="virtualenv"> virtualenv</a>
Install [virtualenv](https://virtualenv.pypa.io/en/latest/): <br>
`sudo python3.8 -m pip install virtualenv` <br>

##### <a name="docker-and-compose"> docker and docker-compose </a>

You'll need git installed (I have been using version 2.25.1).<br>
Install [docker](https://docs.docker.com/engine/install/ubuntu/)  <br>
Here are the list of commands (for ubuntu):
<pre>
   sudo apt-get update
   
   sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common
    
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    
    sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
   
   sudo apt-get update
   sudo apt-get install docker-ce docker-ce-cli containerd.io
</pre>

Configure permissions for docker: <br>
<pre>
  `sudo groupadd docker
   sudo usermod -aG docker $USER
   newgrp docker`
Restart to make those changes work.
</pre>
Install  [docker-compose](https://docs.docker.com/compose/install/#install-compose-on-linux-systems)
Here are the commands needed:
<pre>
sudo curl -L "https://github.com/docker/compose/releases/download/1.26.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
</pre>


#### <a name="directory-structure"> Directory Structure </a>

The kaspy_tools toolset assumes the following directory structure:<br>
<pre>
kaspanet-|-- kaspy_tools
         |-- kaspad
         |-- kasparov
         |-- ...(your code and any code that uses kaspy_tools, e.g: DAGLabs automation_testing)
         |-- venv (a virtualenv environment to run all)
</pre>         
You should create a working directory, let's say we call it here __kaspanet__.<br>
Create a python virtual environment that uses python3.8 under kaspanet:<br>
`virtualenv -p $(which python3.8) venv`

Activate the virtual environment by typing:<br>
`source venv\bin\activate`<br>
Type `python --version` to make sure you have the correct version of python. <br>
Make sure you activate it whenever you run python code or installing libraries.<br>
Use `git clone` to clone repositories to place: <br>
<pre>
  git clone https://github.com/kaspanet/kaspad
  git clone https://github.com/kaspanet/kasparov
  git clone https://github.com/kaspanet/kaspy_tools
</pre>
If you intend to run tests, clone also automation testing:
<pre>
  git clone kaspy_tools: https://github.com/kaspanet/automation_testing 
</pre>

#### <a name="instal-dependencies"> Install Dependencies </a>
First, make sure that your venv is activated. <br>
Install python library dependencies defined in [requirements.txt](https://github.com/kaspanet/kaspy_tools/blob/master/requirements.txt). <br>
<pre>
   < cd into kaspanet/kaspy_tools >
   pip install -r requirements.txt 
</pre>
If you are running automation_tests, install the requirements defined there. <br>
(This may require more libraries to install, needed for pygraphviz.)
Please look at the install-2.sh script)
<pre>
   < cd into kaspanet/automation_testing >
   pip install -r requirements.txt 
</pre>
You should have your own requirements.txt file in your own code as well.

#### <a name="environment-variables"> Set Environment Variables </a>
Define PYTHONPATH, to hold search path targets for python modules. <br>
Add the directory where kaspy_tools resides (kaspanet in out example). <br>
<pre>
   export PYTHONPATH=~/path/to/kaspanet/
</pre>
Add this line to your ~/.bashrc file, to make it persistent.

### <a name="local-conf-files">Prepare Local configuration files </a>
#### <a name="kaspy-tools-constants">kaspy_tools_constants.py </a>
This file contains constants required in various places in kaspy_tools.
You should base your file on kaspy_tools_constants_example.py (or rename that file.)

#### <a name="docker-compose">docker-compose.yaml </a>
This file contains configuration needed to run local containers of various components.<br>
You should base your file on docker-compose-template.yaml (or rename that file.) <br>
Consider editing: <br>
 * SUDO_PASSWORD - set to your sudo password
 * KASPANET_TOP_PATH - set to the location of the top kaspanet directory


### <a name="local_run">Running Locally</a>
The kaspy_tools toolset allows you to run kaspanet components locally in docker containers. <br>
It can build required images, and run them in various scenarios. <br>

#####  <a name="build-kasoad">Build kaspad</a>

Build the kaspad image(s) by running the following command: <br>
(make sure you have activated your environment)
<pre>
  cd ~/kaspanet/local_run/kaspad_docker
  python build_kaspad.py <kaspad-git-commit-number>
  for example:
  python build_kaspad.py v0.6.0
</pre>
If you ommit the commit number, the command will use the KASPAD_BRANCH constant from 
kaspy_tools_constants.py   
The created images will include a kaspad:latest.

##### <a name="build-kasparov">Build kasparov</a>

Build the kaspad image(s) by running the following command: <br>
(make sure you have activated your environment)
<pre>
  cd ~/kaspanet/local_run/kasparov_docker
  python build_kasparov.py <kasparov-git-commit-number>
  for example:
  python build_kasparov.py v0.6.0
</pre>
If you ommit the commit number, the command will use the KASPAROV_BRANCH constant from 
kaspy_tools_constants.py
The created images will include: <br>
- kasparovd:latest <br>
- kasparov-sync:latest <br>

##### <a name="run-services">Run Services</a>

Running services is based on a docker-compose yaml file.
There is a template file called docker-compose-template.yaml, that you
should use in order to create docker-compose.yaml.
Edit the `volumes:` part to configure correct directory names in you host. <br>
Example: <br>
<pre>
    volumes:
      - ~/volumes/build/:/root/.kaspad
      - ~/kaspanet/kaspy_tools/local_run/run_local_services/keys:/go/src/github.com/kaspanet/devops/devnet/common
</pre>
The last line means that ~/kaspanet/kaspy_tools/local_run/run_local_services/kyes is the correct
directory where keys are stored in your system, so kaspad container will map that directory.
   

### <a name="JSON-RPC">JSON-RPC</a>
There are various functions that you can use to send json-rpc messages
to kaspad, and receive results.
These can be found in kaspy_tools/kaspad/json_rpc/rson_rpc_requests.py

### <a name="kaspanet_addresses">Kaspanet Addresses</a>
Kaspanet addresses are based on the
https://github.com/kaspanet/kaspy_tools/blob/master/kaspa_model/kaspa_address.py module.
There is an example here: 
https://github.com/kaspanet/kaspy_tools/blob/master/examples/kaspa_address_examples.py


