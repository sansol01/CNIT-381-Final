import os
import sys
import subprocess


#Updates the interface with new ip and sends a ping.
def ping():
    x=1
    if x == 1:
        os.system("sh ping_run.sh")

#Monitors ping results and updates vpn configuration
def monitor():
    with open("CSR1.txt","r") as temp:
        test=temp.readlines()
    pinged=test[3]
    ping_result=pinged[29:32]
    required_ping = "5/5"
    if ping_result != required_ping:
        os.system("sh monitor_skill_run.sh")


