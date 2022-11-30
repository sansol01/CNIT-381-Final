
import os
import sys
import subprocess

with open("CSR1.txt","r") as temp:
    test=temp.readlines()
pinged=test[3]

ping_result=pinged[29:32]

required_ping = "5/5"
if ping_result != required_ping:
   os.system("sh monitor_skill_run.sh")
