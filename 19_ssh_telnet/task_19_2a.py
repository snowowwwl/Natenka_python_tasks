# -*- coding: utf-8 -*-
'''
Задание 19.2a

Дополнить функцию send_config_commands из задания 19.2

Добавить аргумент verbose, который контролирует будет ли результат
выполнения команд выводится на стандартный поток вывода.

По умолчанию, результат должен выводиться.
'''
#'<br/>'.join(['%s:: %s' % (key, value) for (key, value) in d.items()])



import netmiko
from netmiko import ConnectHandler
import yaml
from pprint import pprint

with open('devices.yaml') as f:
    devices = yaml.safe_load(f)
pprint(devices)
commands = ['interface',
            'export compact']


def send_show_command(dev, com, verbose = 'yes'):
    result_dict = {}
    with ConnectHandler(**dev) as ssh:
        ssh.enable()
        result = ssh.send_config_set(com)
        key = dev['ip']
        result_dict[key] = result
    if (verbose == 'yes'):
        print("\n".join([str for str in result_dict.values()]))
    return result_dict


try:
    for device in devices['routers']:
        send_show_command(device, commands)

except netmiko.ssh_exception.NetMikoAuthenticationException:
    print("Login or pass are not valid. Please check login/pass.")
except netmiko.ssh_exception.NetMikoTimeoutException:
    print("Connection to device {} timed-out".format(device['ip']))