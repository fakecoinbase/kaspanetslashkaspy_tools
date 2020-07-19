
# KASPY_TOOLS

A set of tools that makes it easier to run and use kaspanet tools (kaspad, kasparov).

* [Getting Started](#getting-started)
  * [Getting the required tools](#getting-tools)
    * [Python and PIP](#python-pip)
    * [virtualenv](#virtualenv)
    * [docker and docker-compose]($docker-and-compose )
  * [Directory Structure](#directory-structure)
  * [Install Dependencies](#instal-dependencies)
  * [set environment variables](#environment-variables)
  * [Prepare Local configuration files](#local-conf-files)
    * [kaspy_tools_constants.py](#kaspy-tools-constants)
    * [docker-compose.yaml](#docker-compose)
* Current tools and utilities:
  * [Running locally](#local_run)
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
<pre>
Configure permissions for docker: <br>
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
`virtualenv -p /path/to/python3.8  venv`<br>
(You can use `which python3.8` to discover the location of the interpreter) <br>

Activate the virtual environment by typing:<br>
`source venv\bin\activate`<br>
Type `python --version` to make sure you have the correct version of python. <br>
Make sure you activate it whenever you run python code or installing libraries.<br>
Use `git clone` to clone repositories to place: <br>
kaspad: https://github.com/kaspanet/kaspad <br>
kasparov: https://github.com/kaspanet/kasparov <br>
kaspy_tools: https://github.com/kaspanet/kaspy_tools <br>

#### <a name="instal-dependencies"> Install Dependencies </a>
First, make sure that your venv is activated. <br>
Install python library dependencies defined in [requirements.txt](https://github.com/kaspanet/kaspy_tools/blob/master/requirements.txt). <br>
`pip install -r requirements.txt` <br>
If you are running automation_tests, install the requirements defined there. <br>
You should have your own requirements.txt file in your own code as well.

#### <a name="environment-variables"> Set Environment Variables </a>
Define PYTHONPATH, to hold search path targets for python modules. <br>
Add the directory where kaspy_tools resides (kaspanet in out example). <br>
<pre>
   export PYTHONPATH=~/path/to/kaspanet/
</pre>

### <a name="local-conf-files">Prepare Local configuration files </a>
#### <a name="kaspy-tools-constants">kaspy_tools_constants.py </a>
This file contains constants required in various places in kaspy_tools.
You should base your file on kaspy_tools_constants_example.py (or rename that file.)

#### <a name="docker-compose">docker-compose.yaml </a>
This file contains configuration needed to run local containers of various components.<br>
You should base your file on docker-compose-template.yaml (or rename that file.) <br>
Consider editing: <br>
 * SUDO_PASSWORD

### <a name="local_run">Running Locally</a>
The kaspy_tools toolset allows you to run kaspanet components locally in docker containers. <br>
Tools can build required images, and run them in various scenarios. <br>
Refer to https://github.com/kaspanet/kaspy_tools/blob/master/local_run/local_run.MD
for further explanations.
   

### <a name="JSON-RPC">JSON-RPC</a>
There are various functions that you can use to send json-rpc messages
to kaspad, and receive results.
These can be found in kaspy_tools/kaspad/json_rpc/rson_rpc_requests.py

### <a name="kaspanet_addresses">Kaspanet Addresses</a>
Kaspanet addresses are based on the
https://github.com/kaspanet/kaspy_tools/blob/master/kaspa_model/kaspa_address.py module.
There is an example here: 
https://github.com/kaspanet/kaspy_tools/blob/master/examples/kaspa_address_examples.py


