# -*- coding: utf-8 -*-
"""
Задание 20.3

Создать функцию send_command_to_devices, которая отправляет
разные команды show на разные устройства в параллельных потоках,
а затем записывает вывод команд в файл.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* commands_dict - словарь в котором указано на какое устройство отправлять какую команду. Пример словаря - commands
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


Для выполнения задания можно создавать любые дополнительные функции.

Проверить работу функции на устройствах из файла devices.yaml и словаре commands
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
    start_msg = '===> {} Connection: {}'
    received_msg = '<=== {} Received:   {}'
    ip = device_dict['ip']
    logging.info(start_msg.format(datetime.now().time(), ip))
    try:
        with ConnectHandler(**device_dict) as ssh:
            ssh.enable()
            result = ssh.send_command(command)
            print(result)
            logging.info(received_msg.format(datetime.now().time(), ip))
        return {ip:result}
    except NetMikoAuthenticationException as err:
        logging.warning(err)
        return {ip:str(err)}
    except NetMikoTimeoutException as timeout:
        logging.warning(timeout)
        return {ip:str(timeout)}


def send_command_to_devices(devices, commands_dict, filename, limit):
    data={}
    with ThreadPoolExecutor(max_workers=limit) as executor:
        future_list = []
        for device in devices:
            future = executor.submit(send_show, device, commands_dict[device["ip"]])
            future_list.append(future)

    with open(filename, "w") as file:
        for f in as_completed(future_list):
            result = f.result()
            data.update(result)
        for ip, command in commands_dict.items():
            head = "DeviceIP: "+ip+" Command: "+ command+'\n'
            file.write(head)
            file.writelines(data[ip])
            file.write("\n")


if __name__ == '__main__':
    with open('devices.yaml') as f:
        devices = yaml.safe_load(f)
    commands = {'192.168.88.1': 'system',
                '192.168.88.2': 'interface',
                '192.168.88.3': 'ping 8.8.8.8 count 2'
                }
    #for device in devices:
    #   print(send_show(device, command))
    send_command_to_devices(devices, commands, "task_20_3_result.txt", 3)

