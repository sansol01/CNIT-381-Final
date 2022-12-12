from netmiko import ConnectHandler
import myparamiko as m
import time
import threading
import getpass
import routers

r1 = { # Branch router
        'device_type': 'cisco_ios',
        'host': '192.168.56.103', 
        'username': 'cisco',
        'password': 'cisco123!',
        'port': 22,
        'secret': 'cisco123!',
        'verbose': True
    }
r2 = { # HQ router
        'device_type': 'cisco_ios',
        'host': '192.168.56.101', 
        'username': 'cisco',
        'password': 'cisco123!',
        'port': 22,
        'secret': 'cisco123!',
        'verbose': True
    }

def backup(message):    # this function determines which router to backup

    if "Branch" in message: # if Branch is specified, Branch will be backed up
        return "Backup for Branch file location: " + backupR(r1)  
    elif "HQ" in message:   # if HQ is specified, HQ will be backed up
        return "Backup for HQ file loaction: " + backupR(r2)  
    elif "all" in message:  # is the all option is specified it will perform a backup off all the routers
        return ("Backup of all routers performed:\n" + "Branch file loaction: " + backupR(r1) + "\n HQ file location" + backupR(r2)) # if there was no specification or all was specified all routers will be backed up
    else:                   # if no routers were specified it will give error message detailing it is case sensitive and the options availible.
        return 'I am case-sensitive! Do "Branch" for Branch router, "HQ" for HQ router, and "all" for all rotuers.\n IMPORTANT! NO BACKUPS WERE MADE!!'


def backupR(targetR):
    connection = ConnectHandler(**targetR)  # connects to the choosen router
    connection.enable() # makes sure that the router is in privlige exec mode
    print('Sending commands...')
    output = connection.send_command('show run') # displays the running configuration it to the variable output
    output_list = output.splitlines()   # splits output into seprate lines for readability
    output_list = output_list[9:-1]     # takes away some of the unnecessary lines at the top
    output = '\n'.join(output_list)
    print(output_list)

    from datetime import datetime   # gets the current time and stores them to easier to use variables
    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day
    hour = now.hour
    minute = now.minute

    filename = f'ROUTER_BACKUP/{targetR["host"]}_{year}-{month}-{day}-{hour}-{minute}.txt'  # determines the name of the backup file using IP address and current date for version control
    with open(filename, 'w') as f:
        f.write(output) # writes and stores the backup config file

    output = connection.send_command_timing('copy run start') # stores a local copy of the running-config to the startup-config NVRAM.

    print('Closing connection')
    connection.disconnect()
    print('#'*40)

    return filename


