# -*- coding: utf-8 -*-
'''
Задание 19.2

Создать функцию send_config_commands

Функция подключается по SSH (с помощью netmiko) к устройству и выполняет перечень команд в конфигурационном режиме
на основании переданных аргументов.

Параметры функции:
* device - словарь с параметрами подключения к устройству
* config_commands - список команд, которые надо выполнить

Функция возвращает словарь с результатами выполнения команды:
* ключ - IP устройства
* значение - вывод с выполнением команд

Отправить список команд commands на все устройства из файла devices.yaml (для этого надо считать информацию из файла) с помощью функции send_config_commands.

'''


import netmiko
from netmiko import ConnectHandler
import yaml
from pprint import pprint

with open('devices.yaml') as f:
    devices = yaml.safe_load(f)
pprint(devices)
commands = ['interface',
            'export compact']


def send_show_command(dev, com):
    result_dict = {}
    with ConnectHandler(**dev) as ssh:
        ssh.enable()
        result = ssh.send_config_set(com)
        key = dev['ip']
        result_dict[key] = result
        return result_dict


try:
    for device in devices['routers']:
        pprint(send_show_command(device, commands))

except netmiko.ssh_exception.NetMikoAuthenticationException:
    print("Login or pass are not valid. Please check login/pass.")
except netmiko.ssh_exception.NetMikoTimeoutException:
    print("Connection to device {} timed-out".format(device['ip']))