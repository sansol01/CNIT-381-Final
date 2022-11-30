from netmiko import ConnectHandler
import myparamiko as m
import time
import threading
import getpass

#start = time.time()
#r1 = manager.connect(**routers.router1)
#r2 = manager.connect(**routers.router2)

r1 = {
        'device_type': 'cisco_ios',
        'host': '192.168.56.102', 
        'username': 'cisco',
        'password': 'cisco123!',
        'port': 22,
        'secret': 'cisco123!',
        'verbose': True
    }

r2 = {
        'device_type': 'cisco_ios',
        'host': '192.168.56.107', 
        'username': 'cisco',
        'password': 'cisco123!',
        'port': 22,
        'secret': 'cisco123!',
        'verbose': True
    }

def backup(message):
    if "all" in message:
        #backupR(r2)
        #backupR(r1)
        return ("Backing up all routers\n" + "File loaction: " + backupR(r1) + "\nFile location" + backupR(r2))
    elif "r2" in message:
        return "File loaction: " + backupR(r2) 
    else: #default to r1
        return "File location: " + backupR(r1)


def backupR(rTarget):
    #cut toggle out of the string

    #Check for a target router
#    if "r2" in message:
#        rTarget = r2
#    else: #default to r1
#        rTarget = r1

    #call toggle_interface and return the result
    connection = ConnectHandler(**rTarget)
    #prompt = connection.find_prompt()
    #if '>' in prompt:
    connection.enable()
    print('Sending commands...')
    #output = connection.send_command('copy run start')
    output = connection.send_command('sho run')
    output_list = output.splitlines()
    output_list = output_list[9:-1]
    output = '\n'.join(output_list)
    print(output_list)

    from datetime import datetime
    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day
    hour = now.hour
    minute = now.minute

    filename = f'ROUTER_BACKUP/{rTarget["host"]}_{year}-{month}-{day}-{hour}-{minute}.txt'
    with open(filename, 'w') as f:
        f.write(output)

    print('Closing connection')
    connection.disconnect()
    print('#'*40)

    return filename

#routers = m.get_list_from_file ('routers.txt')
#threads = list()
#for router in routers:
#    th = threading.Thread(target = backup, args = (router,))
#    threads.append(th)

#for th in threads:
#    th.start()

#for th in threads:
#    th.join()

#end = time.time()
#print(f'Total execution time: {end-start}')


