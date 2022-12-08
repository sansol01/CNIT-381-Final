#!/bin/bash

cd ~/

# Runs the playbook.
if true;then
    ansible-playbook CHANGE_VPN_CONFIG.yml -i hosts

fi

