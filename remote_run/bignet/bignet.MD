### BIGNET

This tool makes it possible to run 100 bundles of kaspanet tools.

##### Principles:
 - in bundle: kasparov-sync, kasparovd, postgresql, kaspad, miner, wallet
 - Each bundle in a single instance of ec2
 - Use auto scaling group to run 100 instances
 - A single instance to run dns seeder
 - Use cloudformation to define resources
 - Add a subnet to current VPC to host all bundles
 
 
##### Preparations
 - create S3
 - compile tools in the requested version (branch) and load into aws ECR  
    (Elastic Container Registry)

#### Usage:
##### Credentials

Fill the correct values in the aws credentials fields in your kaspy_tools_constants.py .
See the parameter names in the kaspy_tools_constants_example.py file.