# -*- coding: utf-8 -*-
"""
Задание 19.3

Создать функцию send_commands (для подключения по SSH используется netmiko).

Параметры функции:
* device - словарь с параметрами подключения к устройству, которому надо передать команды
* show - одна команда show (строка)
* filename - имя файла, в котором находятся команды, которые надо выполнить (строка)
* config - список с командами, которые надо выполнить в конфигурационном режиме

В зависимости от того, какой аргумент был передан, функция вызывает разные функции внутри.
При вызове функции, всегда будет передаваться только один из аргументов show, config, filename.

Далее комбинация из аргумента и соответствующей функции:
* show - функция send_show_command из задания 19.1
* config - функция send_config_commands из задания 19.2
* filename - функция send_commands_from_file (ее надо написать по аналогии с предыдущими)

Функция возвращает словарь с результатами выполнения команды:
* ключ - IP устройства
* значение - вывод с выполнением команд

Проверить работу функции на примере:
* устройств из файла devices.yaml (для этого надо считать информацию из файла)
* и различных комбинация аргумента с командами:
    * списка команд commands
    * команды command
    * файла config.txt

"""


import netmiko
from netmiko import ConnectHandler
import yaml
from pprint import pprint


commands = ['interface',
            'export compact']
command = 'interface'

with open('devices.yaml') as f:
    devices = yaml.safe_load(f)

def send_show_command(dev, com):
    result_dict = {}
    with ConnectHandler(**dev) as ssh:
        ssh.enable()
        result = ssh.send_command(com)
        key = dev['ip']
        result_dict[key] = result
        return result_dict

def send_config_commands(dev, com):
    result_dict = {}
    with ConnectHandler(**dev) as ssh:
        ssh.enable()
        result = ssh.send_config_set(com)
        key = dev['ip']
        result_dict[key] = result
        return result_dict

def send_config_fromfile(dev, filenm):
    result_dict = {}
    with ConnectHandler(**dev) as ssh:
        ssh.enable()
        result = ssh.send_config_from_file(filenm)
        key = dev['ip']
        result_dict[key] = result
        return result_dict

def send_commands(device, show = None, config = None, filename = None):
    result_dict = {}
    if show and not config and not filename:
        result_dict = send_show_command(device, show)
    elif config and not show and not filename:
        result_dict = send_config_commands(device, config)
    elif filename and not show and not config:
        result_dict = send_config_fromfile(device, filename)
    else:
        print('Please enter only one parametr show/filename/config')
    return result_dict


try:
    for dev in devices['routers']:
        print("Command:")
        pprint(send_commands(dev, show = command))
        print("Set of commands:")
        pprint(send_commands(dev, config = commands))
        print("Set of commands from file:")
        pprint(send_commands(dev, filename = 'config_set.txt'))
        print("Wrong parametr:")
        pprint(send_commands(dev, show = command, config = commands))

except netmiko.ssh_exception.NetMikoAuthenticationException:
    print("Login or pass are not valid. Please check login/pass.")
except netmiko.ssh_exception.NetMikoTimeoutException:
    print("Connection to device {} timed-out".format(dev['ip']))

