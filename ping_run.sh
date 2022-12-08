#!/bin/bash

cd ~/
# Runs the playbook.
if true;then
    ansible-playbook CHANGE_IP_PING.yml -i hosts

fi

