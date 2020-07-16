
# KASPY_TOOLS

A set of tools that makes it easier to run and use kaspanet tools (kaspad, kasparov).

* [Getting Started](#getting-started)
  * [Getting the required tools](#getting-tools)
  * [Directory Structure](#directory-structure)
  * [Install Dependencies](#instal-dependencies)
  * [Local configuration files](#local-conf-files)
    * [kaspy_tools_constants.py](#kaspy-tools-constants)
    * [docker-compose.yaml](#docker-compose)    
* Current tools and utilities:
  * [Running locally](#local_run)
    * Create kaspad docker image
    * Create kasparov docker images (kasparov-sync, kasparovd)
    * running services locally: 
      * a pair of kaspad instances (one with non-volatile storage)
      * single set of kasparov services
      * postgres DB for kasparov
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
Current kaspy_tools requires python version 3.8.0 and on.<br>
Here's a [convenient way to install it on ubuntu](https://linuxize.com/post/how-to-install-python-3-8-on-ubuntu-18-04/). <br>
(Do not try to remove the version pre-installed on your system!!!)<br> 

Make sure you also have pip3 installed:<br>
`sudo apt install python3-pip`<br>

Then upgreade pip:<br>
`python3 -m pip install --upgrade pip`<br>

Install [virtualenv](https://virtualenv.pypa.io/en/latest/): <br>
`sudo pip3 install virtualenv`<br>

You'll need git installed (I have been using version 2.25.1).<br>
Install [docker](https://docs.docker.com/engine/install/ubuntu/) 
and [docker-compose](https://docs.docker.com/compose/install/#install-compose-on-linux-systems)
.<br>


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

Install python library dependencies defined in [requirements.txt](https://github.com/kaspanet/kaspy_tools/blob/master/requirements.txt). <br>
`pip install -r requirements.txt` <br>
If you are running automation_tests, install the requirements defined there. <br>
You should have your own requirements.txt file in your own code as well.

### <a name="local-conf-files">Local configuration files </a>
#### <a name="kaspy-tools-constants">kaspy_tools_constants.py </a>
This file contains constants required in various places in kaspy_tools.
You should base your file on kaspy_tools_constants_example.py (or rename that file.)

#### <a name="docker-compose">docker-compose.yaml </a>
This file contains configuration needed to run local containers of various components.<br>
You should base your file on docker-compose-template.yaml (or rename that file.)

### <a name="local_run">Running Locally</a>
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


