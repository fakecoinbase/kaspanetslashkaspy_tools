#!/bin/bash
#
# Manual steps to perform after script 1,2 :
#
# manually clone automation_testing
# cd kaspanet
# source venv/bin/activate
# cd automation_testing
# pip install -r requirements.txt
# mv kaspy_tools_constants_example.py  kaspy_tools_constants.py
# mv kaspy_tools/local_run/run_local_services/docker-compos-templatese.yaml kaspy_tools/local_run/run_local_services/docker-compos.yaml
# cd kaspy_tools/local_run/kaspad
# python build_kaspad.py
# cd kaspy_tools/local_run/kasparov_docker
# python build_kasparov.py
#
#
# cd kaspanet/automation_testing/test_suites
# pytest test_suite_01.....
