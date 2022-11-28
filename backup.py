from netmiko import ConnectHandler
import myParamiko as m
import encrypt_dev_info as edi
import time
import threading
import getpass

start = time.time()

def backup(router):
    connection = ConnectHandler(**router)
    prompt = connection.find_prompt()
    if '>' in prompt:
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

    filename = f'{router["host"]}_{year}-{month}-{day}-{hour}-{minute}.txt'
    with open(filename, 'w') as f:
        f.write(output)

    print('Closing connection')
    connection.disconnect()
    print('#'*40)

routers = m.get_list_from_file ('routers.txt')
threads = list()
for router in routers:
    th = threading.Thread(target = backup, args = (router,))
    threads.append(th)

for th in threads:
    th.start()

for th in threads:
    th.join()

end = time.time()
print(f'Total execution time: {end-start}')
