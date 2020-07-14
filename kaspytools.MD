#KASPY_TOOLS

A set of tools that makes it easier to run and use kaspanet tools (kaspad, kasparov).

###Current tools and utilities:
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
  
* [Getting Started](#getting-started)
  * Based on kaspy_tools/kaspy_tools_constants_example.py, create your own kaspy_tools/kaspy_tools_constants.py .
  

###<a name="local_run">Running Locally</a>
Refer to https://github.com/kaspanet/kaspy_tools/blob/master/local_run/local_run.MD
for further explanations.

###<a name="JSON-RPC">JSON-RPC</a>
There are various functions that you can use to send json-rpc messages
to kaspad, and receive results.
These can be found in kaspy_tools/kaspad/json_rpc/rson_rpc_requests.py

###<a name="kaspanet_addresses">Kaspanet Addresses</a>
Kaspanet addresses are based on the
https://github.com/kaspanet/kaspy_tools/blob/master/kaspa_model/kaspa_address.py module.
There is an example here: 
https://github.com/kaspanet/kaspy_tools/blob/master/examples/kaspa_address_examples.py


###<a name="getting-started">Getting Started</a>
Based on kaspy_tools/kaspy_tools_constants_example.py, create your own kaspy_tools/kaspy_tools_constants.py .
