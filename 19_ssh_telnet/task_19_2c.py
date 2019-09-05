# -*- coding: utf-8 -*-
'''
Задание 19.2c

Переделать функцию send_config_commands из задания 19.2b

Если при выполнении команды возникла ошибка,
спросить пользователя надо ли выполнять остальные команды.

Варианты ответа [y]/n:
* y - выполнять остальные команды (значение по умолчанию)
* n - не выполнять остальные команды

Функция send_config_commands по-прежнему должна возвращать кортеж из двух словарей:
* первый словарь с выводом команд, которые выполнились без ошибки
* второй словарь с выводом команд, которые выполнились с ошибками


Оба словаря в формате
* ключ - команда
* значение - вывод с выполнением команд

Проверить функцию на командах с ошибкой.

'''

import netmiko
from netmiko import ConnectHandler
import yaml
from pprint import pprint

with open('devices.yaml') as f:
    devices = yaml.safe_load(f)
pprint(devices)
bad_dict = {}
good_dict = {}
commands_with_errors = ['show ip int br', 'show run' ]
correct_commands = ['interface',
            'export compact']
commands = commands_with_errors + correct_commands

def send_show_command(dev, com, verbose = 'yes'):
    good_result_dict = {}
    bad_result_dict = {}
    with ConnectHandler(**dev) as ssh:
        ssh.enable()
        for command in com:
            result = ssh.send_command(command)
            if 'bad command' in result:
                answer = input('The command {} is bad. Proceed? Enter [y/n]'.format(command))
                if answer=='n':
                    print('You choose stop the program. The function will return empty dictionaries.')
                    break
                else:
                    key = command
                    bad_result_dict[key] = result
            else:
                key = command
                good_result_dict[key] = result
    if (verbose == 'yes'):
        print("\n".join([str for str in good_result_dict.values()]))
    return bad_result_dict, good_result_dict


try:
    for device in devices['routers']:
        bad_dict, good_dict = send_show_command(device, commands, 'yes')
        pprint(bad_dict)
        pprint("*****")
        pprint(good_dict)
except netmiko.ssh_exception.NetMikoAuthenticationException:
    print("Login or pass are not valid. Please check login/pass.")
except netmiko.ssh_exception.NetMikoTimeoutException:
    print("Connection to device {} timed-out".format(device['ip']))