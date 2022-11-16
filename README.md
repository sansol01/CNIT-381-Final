# CNIT-381-Final
***Purpose:*** 
This is the repoitory for R. Berends, J. Sletten, S. Solsvik final project for CNIT 381 Network Programmability and Automation.

# Project descriptoion

Create a chatbot that can administer a network using Paramiko/Netmiko, Netconf/Restconf, and Ansible.

***Problem:***
A branch of a Bank can only get an ADSL connection to the internet. They need to use a VPN tunnel for secure access to the HQ to access client data.
Becasue of the connection the branch has their public IP address changes every 3 hours dropping their VPN connection. 
Part of the chatbots purpose it to notify the IT administrator at the brach that a new IP address has been assigned and to then automatically change the VPN configuration to use this new IP address to regain secure VPN access to HQ.
