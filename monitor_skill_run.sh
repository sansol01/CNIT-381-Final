#!/bin/bash

cd ~/CNIT-381-Final

# Runs the playbook.
if true;then
    ansible-playbook CHANGE_VPN_CONFIG.yml -i hosts

fi

