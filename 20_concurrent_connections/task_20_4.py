# -*- coding: utf-8 -*-
"""
Задание 20.4

Создать функцию send_commands_to_devices, которая отправляет команду show или config на разные устройства в параллельных
 потоках, а затем записывает вывод команд в файл.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* show - команда show, которую нужно отправить (по умолчанию, значение None)
* config - команды конфигурационного режима, которые нужно отправить (по умолчанию, значение None)
* filename - имя файла, в который будут записаны выводы всех команд
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция ничего не возвращает.

Вывод команд должен быть записан в файл в таком формате (перед выводом команды надо написать имя хоста и саму команду):

R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R2#sh arp
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  192.168.100.1          76   aabb.cc00.6500  ARPA   Ethernet0/0
Internet  192.168.100.2           -   aabb.cc00.6600  ARPA   Ethernet0/0
Internet  192.168.100.3         173   aabb.cc00.6700  ARPA   Ethernet0/0
R3#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.3   YES NVRAM  up                    up
Ethernet0/1                unassigned      YES NVRAM  administratively down down

Пример вызова функции:
In [5]: send_commands_to_devices(devices, show='sh clock', filename='result.txt')

In [6]: cat result.txt
R1#sh clock
*04:56:34.668 UTC Sat Mar 23 2019
R2#sh clock
*04:56:34.687 UTC Sat Mar 23 2019
R3#sh clock
*04:56:40.354 UTC Sat Mar 23 2019

In [11]: send_commands_to_devices(devices, config='logging 10.5.5.5', filename='result.txt')

In [12]: cat result.txt
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#logging 10.5.5.5
R1(config)#end
R1#config term
Enter configuration commands, one per line.  End with CNTL/Z.
R2(config)#logging 10.5.5.5
R2(config)#end
R2#config term
Enter configuration commands, one per line.  End with CNTL/Z.
R3(config)#logging 10.5.5.5
R3(config)#end
R3#

In [13]: send_commands_to_devices(devices,
                                  config=['router ospf 55', 'network 0.0.0.0 255.255.255.255 area 0'],
                                  filename='result.txt')

In [14]: cat result.txt
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#router ospf 55
R1(config-router)#network 0.0.0.0 255.255.255.255 area 0
R1(config-router)#end
R1#config term
Enter configuration commands, one per line.  End with CNTL/Z.
R2(config)#router ospf 55
R2(config-router)#network 0.0.0.0 255.255.255.255 area 0
R2(config-router)#end
R2#config term
Enter configuration commands, one per line.  End with CNTL/Z.
R3(config)#router ospf 55
R3(config-router)#network 0.0.0.0 255.255.255.255 area 0
R3(config-router)#end
R3#


Для выполнения задания можно создавать любые дополнительные функции.
"""


from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import time
from itertools import repeat
import logging
import yaml
from netmiko import ConnectHandler, NetMikoAuthenticationException, NetMikoTimeoutException


logging.getLogger('paramiko').setLevel(logging.WARNING)

logging.basicConfig(
    format = '%(threadName)s %(name)s %(levelname)s: %(message)s',
    level=logging.INFO)

def send_show(device_dict, command):
    result_dict = {}
    start_msg = '===> {} Connection: {}'
    received_msg = '<=== {} Received:   {}'
    ip = device_dict['ip']
    logging.info(start_msg.format(datetime.now().time(), ip))
    try:
        with ConnectHandler(**device_dict) as ssh:
            ssh.enable()
            result = ssh.send_command(command)
            result_dict[ip] = result
            logging.info(received_msg.format(datetime.now().time(), ip))
        return result_dict
    except NetMikoAuthenticationException as err:
        logging.warning(err)
        result_dict[ip] = str(err)
        return result_dict
    except NetMikoTimeoutException as timeout:
        logging.warning(timeout)
        result_dict[ip] = str(timeout)
        return result_dict

def send_config(device_dict, command_list):
    result_dict = {}
    start_msg = '===> {} Connection: {}'
    received_msg = '<=== {} Received:   {}'
    ip = device_dict['ip']
    logging.info(start_msg.format(datetime.now().time(), ip))
    try:
        with ConnectHandler(**device_dict) as ssh:
            ssh.enable()
            result = ssh.send_config_set(command_list)
            result_dict[ip] = result
            logging.info(received_msg.format(datetime.now().time(), ip))
        return result_dict
    except NetMikoAuthenticationException as err:
        logging.warning(err)
        result_dict[ip] = str(err)
        return result_dict
    except NetMikoTimeoutException as timeout:
        logging.warning(timeout)
        result_dict[ip] = str(timeout)
        return result_dict


def send_commands_to_devices(devices, show = None, config = None, filename = "result.txt", limit = 3):
    data={}

    with ThreadPoolExecutor(max_workers=limit) as executor:
        future_list = []
        if show:
            for device in devices:
                if type(show) == list:
                    future = executor.submit(send_config, device, show)
                    future_list.append(future)
                else:
                    future = executor.submit(send_show, device, show)
                    future_list.append(future)
        if config:
            for device in devices:
                if type(config) == list:
                    future = executor.submit(send_config, device, config)
                    future_list.append(future)
                else:
                    future = executor.submit(send_show, device, config)
                    future_list.append(future)
    with open(filename, "a") as file:
        for f in as_completed(future_list):
            result = f.result()
            data.update(result)
        for device in devices:
            file.write("*************************\n")
            if type(show) == list:
                for sh in show:
                    head = "DeviceIP: "+device["ip"]+" Command: "+ sh+'\n'
                    file.write(head)
                    file.writelines(data[device["ip"]])
                    file.write("\n")
            if type(show) == str:
                head = "DeviceIP: " + device["ip"] + " Command: " + show + '\n'
                file.write(head)
                file.writelines(data[device["ip"]])
                file.write("\n")
            if type(config) == list:
                for cf in config:
                    head = "DeviceIP: "+device["ip"]+" Command: "+ cf+'\n'
                    file.write(head)
                    file.writelines(data[device["ip"]])
                    file.write("\n")
            if type(config) == str:
                head = "DeviceIP: " + device["ip"] + " Command: " + config + '\n'
                file.write(head)
                file.writelines(data[device["ip"]])
                file.write("\n")

if __name__ == '__main__':
    with open('devices.yaml') as f:
        devices = yaml.safe_load(f)
    send_commands_to_devices(devices, show='system', filename = "task_20_4_result.txt")
    send_commands_to_devices(devices, config='ping 8.8.8.8 count 2', filename="task_20_4_result.txt")
    send_commands_to_devices(devices, config=['ping 9.9.9.9 count 2', 'ping 10.10.10.10 count 2'],
                             filename="task_20_4_result.txt")
    send_commands_to_devices(devices, show=['interface', 'export compact'],
                             filename="task_20_4_result.txt")