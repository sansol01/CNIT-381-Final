#!/bin/bash

cd ~/

if true;then
    ansible-playbook CHANGE_IP_PING.yml -i hosts

fi

