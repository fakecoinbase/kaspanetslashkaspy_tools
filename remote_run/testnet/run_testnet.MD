####Configure openvpn
##### client.ovpn file
Connecting to json-rpc at testnet nodes requires running openvpn.
Kaspy tools can run openvpn for you.
You need an active account, and a local client.ovpn configuration file.
For exqample:
I got my file from https://vpn.daglabs.com/

##### login.conf file
This file contains the openvpn user name and password.
Write each one in a seperate line.
Example for user=dave pass=12345
dave
12345

##### Cert file
You should have rpc.cert file under the testnet directory, under the keys directory
that you have configured in the kaspy_tools_constants.py file.
Example:
KEYS_PATH = os.path.expanduser("~/keys")
so, put the file here:
~/keys/testnet/rpc.cert





