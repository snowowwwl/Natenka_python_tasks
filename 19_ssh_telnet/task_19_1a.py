# -*- coding: utf-8 -*-
"""
Задание 19.1a

Переделать функцию send_show_command из задания 19.1 таким образом,
чтобы обрабатывалось исключение, которое генерируется
при ошибке аутентификации на устройстве.

При возникновении ошибки, должно выводиться сообщение исключения.

Для проверки измените пароль на устройстве или в файле devices.yaml.
"""

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