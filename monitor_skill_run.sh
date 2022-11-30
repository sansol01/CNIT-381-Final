#!/bin/bash

cd ~/labs/devnet-src/ansible/ansible-csr1000v/PING_RESULT

if true;then
    ansible-playbook CHANGE_VPN_CONFIG.yml -i hosts

fi

