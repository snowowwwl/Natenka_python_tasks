# -*- coding: utf-8 -*-
"""
Задание 20.3a

Создать функцию send_command_to_devices, которая отправляет
список указанных команды show на разные устройства в параллельных потоках,
а затем записывает вывод команд в файл.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* commands_dict - словарь в котором указано на какое устройство отправлять какие команды. Пример словаря - commands
* filename - имя файла, в который будут записаны выводы всех команд
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция ничего не возвращает.

Вывод команд должен быть записан в файл в таком формате (перед выводом каждой команды надо написать имя хоста и саму команду):

R2#sh arp
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  192.168.100.1          87   aabb.cc00.6500  ARPA   Ethernet0/0
Internet  192.168.100.2           -   aabb.cc00.6600  ARPA   Ethernet0/0
R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R1#sh arp
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  10.30.0.1               -   aabb.cc00.6530  ARPA   Ethernet0/3.300
Internet  10.100.0.1              -   aabb.cc00.6530  ARPA   Ethernet0/3.100
R3#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.3   YES NVRAM  up                    up
Ethernet0/1                unassigned      YES NVRAM  administratively down down
R3#sh ip route | ex -

Gateway of last resort is not set

      10.0.0.0/8 is variably subnetted, 4 subnets, 2 masks
O        10.1.1.1/32 [110/11] via 192.168.100.1, 07:12:03, Ethernet0/0
O        10.30.0.0/24 [110/20] via 192.168.100.1, 07:12:03, Ethernet0/0


Порядок команд в файле может быть любым.

Для выполнения задания можно создавать любые дополнительные функции, а также использовать функции созданные в предыдущих заданиях.

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


def send_show(device_dict, command_list):
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


def send_command_to_devices(devices, commands_dict, filename, limit):
    data={}
    with ThreadPoolExecutor(max_workers=limit) as executor:
        future_list = []
        for device in devices:
            for command in commands_dict[device["ip"]]:
                future = executor.submit(send_show, device, command)
                future_list.append(future)

    with open(filename, "w") as file:
        for f in as_completed(future_list):
            result = f.result()
            data.update(result)
        print(data)
        for ip, commands in commands_dict.items():
            for command in commands:
                head = "DeviceIP: "+ip+" Command: "+ command+'\n'
                file.write(head)
                file.writelines(data[ip])
                file.write("\n")


if __name__ == '__main__':
    with open('devices.yaml') as f:
        devices = yaml.safe_load(f)
    commands = {'192.168.88.1': ['system'],
                '192.168.88.2': ['interface', 'export compact'],
                '192.168.88.3': ['ping 8.8.8.8 count 2', 'ping 10.10.10.10 count 3']
                }
    #for device in devices:
    #   print(send_show(device, command))
    send_command_to_devices(devices, commands, "task_20_3a_result.txt", 3)

