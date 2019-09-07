# -*- coding: utf-8 -*-
"""
Задание 19.3b


Дополнить функцию send_commands таким образом, чтобы перед подключением к устройствам по SSH,
выполнялась проверка доступности устройства pingом (можно вызвать команду ping в ОС).

> Как выполнять команды ОС, описано в разделе 11_modules/subprocess.html. Там же есть пример функции с отправкой ping.

Если устройство доступно, можно выполнять подключение.
Если не доступно, вывести сообщение о том, что устройство с определенным IP-адресом недоступно
и не выполнять подключение  к этому устройству.

Для удобства можно сделать отдельную функцию для проверки доступности
и затем использовать ее в функции send_commands.
"""



import netmiko
from netmiko import ConnectHandler
import yaml
from pprint import pprint
import subprocess

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


try:
    for dev in devices['routers']:
        print("Command:")
        pprint(send_commands(dev, show=command))
        print("Set of commands:")
        pprint(send_commands(dev, config=commands))
        print("Set of commands from file:")
        pprint(send_commands(dev, filename='config_set.txt'))
        print("Wrong parametr:")
        pprint(send_commands(dev, show=command, config=commands))

except netmiko.ssh_exception.NetMikoAuthenticationException:
    print("Login or pass are not valid. Please check login/pass.")
except netmiko.ssh_exception.NetMikoTimeoutException:
    print("Connection to device {} timed-out".format(dev['ip']))

