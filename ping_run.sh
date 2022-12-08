#!/bin/bash

cd ~/labs/devnet-src/ansible/ansible-csr1000v/PING_RESULT

if true;then
    ansible-playbook CHANGE_IP_PING.yml -i hosts

fi

