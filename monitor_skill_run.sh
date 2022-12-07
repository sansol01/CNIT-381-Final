#!/bin/bash

cd ~/PING_RESULT

if true;then
    ansible-playbook CHANGE_VPN_CONFIG.yml -i hosts

fi

