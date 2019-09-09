# -*- coding: utf-8 -*-
'''
Задание 19.4

Создать функцию send_commands_to_devices (для подключения по SSH используется netmiko).

Параметры функции:
* devices_list - список словарей с параметрами подключения к устройствам, которым надо передать команды
* show - одна команда show (строка)
* filename - имя файла, в котором находятся команды, которые надо выполнить (строка)
* config - список с командами, которые надо выполнить в конфигурационном режиме

В этой функции должен использоваться список словарей, в котором не указаны имя пользователя, пароль, и пароль на enable (файл devices2.yaml).

Функция должна запрашивать имя пользователя, пароль и пароль на enable при старте.
Пароль не должен отображаться при наборе.

Функция send_commands_to_devices должна использовать функцию send_commands из задания 19.3.

'''


import netmiko
from netmiko import ConnectHandler
import yaml
from pprint import pprint
import subprocess
import os
import sys

commands = ['interface',
            'export compact']
command = 'interface'

with open('devices2.yaml') as f:
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

def ping_ip(ip_address):
    """
    Ping IP address and return tuple:
    On success:
        * True
        * command output (stdout)
    On failure:
        * False
        * error output (stderr)
    """
    reply = subprocess.run(['ping', ip_address, '-n', '3'],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           encoding='ascii'
                           )
    if reply.returncode == 0:
        print("Check the ip...Ping ok.")
        return True
    else:
        return False

def send_commands(device, show = None, config = None, filename = None):
    result_dict = {}
    if ping_ip(device['ip']):
        if show and not config and not filename:
            result_dict = send_show_command(device, show)
        elif config and not show and not filename:
            result_dict = send_config_commands(device, config)
        elif filename and not show and not config:
            result_dict = send_config_fromfile(device, filename)
        else:
            print('Please enter only one parametr show/filename/config')
    else:
        print("Ping of ip adress {} return error. Please check the device".format(device['ip']))
    return result_dict

def send_commands_to_devices(device_list, show = None, config = None, filename = None):
    result_dict = {}
    for dev in device_list:
        user = input('Username: ')
        password = input("Enter pass:")
        dev['username'] = user
        dev['password'] = password
        result_dict = send_commands(dev, show, config, filename)
    return result_dict


try:
    print("Command:")
    pprint(send_commands_to_devices(devices['routers'], show=command))
    print("Set of commands:")
    pprint(send_commands_to_devices(devices['routers'], config=commands))
    print("Set of commands from file:")
    pprint(send_commands_to_devices(devices['routers'], filename='config_set.txt'))
    print("Wrong parametr:")
    pprint(send_commands_to_devices(devices['routers'], show=command, config=commands))

except netmiko.ssh_exception.NetMikoAuthenticationException:
    print("Login or pass are not valid. Please check login/pass.")
except netmiko.ssh_exception.NetMikoTimeoutException:
    print("Connection to device {} timed-out".format(devices['routers']['ip']))