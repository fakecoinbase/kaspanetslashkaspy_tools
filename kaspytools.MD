#KASPY_TOOLS

A set of tools that makes it easier to run and use kaspanet tools (kaspad, kasparov).

###Current tools and utilities:
* [Running locally](#local_run)
  * Create kaspad docker image
  * Create kasparov docker images (kasparov-sync, kasparovd)
  * running services locally: 
    * a pair of kaspad instances (one with non volatile storage)
    * single set of kasparov services
    * postgres DB for kasparov
* JSON-RPC communication with kaspad (used with other tools)
* Blocks
  * Creating and submitting a block based on a template from kaspad
  * Parsing a block given in binary form
* 
  

###<a name="local_run">Running Locally</a>
Refer to under kaspy_tools/local_run/local_run.MD for details.