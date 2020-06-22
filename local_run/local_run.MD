## Local Running of kaspanet services

#### Building

Current version of local_run assumes having a 
kaspad and kasparov local repositories at the same level of kaspy_tools.

##### Build kaspad

Go to the main level of kaspad and checkout the desired branch you want
to build (and don't forget to pull).
Then call build_and_tag_kaspad_image() function from make_kaspad.py file   
(you can run the file as __main__).
This should create the image (among other images) kaspad:latest.

##### Build kasparov

Go to the main level of kasparov and checkout the desired branch you want
to build (and don't forget to pull).
Then call build_and_tag_kasparov_services() function from make_kasparov.py file   
(you can run the file as __main__).
This should create two images (among other images): kaspad:latest.
- kasparovd:latest
- kasparov-sync:latest

##### Run Services

Running services is based on a docker-compose yaml file.
This file can be created automatically by calling: 
docker_compose_utils.create_docker_compose_file() method.
There is such a call in local_run/run_services/run_services.py file.
The run_services() method in this file can run all services (including kasparov
services, postgres database and 2 kaspad services).
You can see in it how to run fewer services (by calling run_docker_compose()).

Note:
The local_run/run_all directory is kept for backward compatability only, and
you should not use it.