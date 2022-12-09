#!/bin/bash

cd ~/CNIT-381-Final
# Runs the playbook.
if true;then
    ansible-playbook CHANGE_IP_PING.yml -i hosts

fi

