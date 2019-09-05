# -*- coding: utf-8 -*-
'''
Задание 19.2d

В этом задании надо создать функцию send_cfg_to_devices, которая выполняет команды на нескольких устройствах
последовательно и при этом выполняет проверку на ошибки в командах.

Параметры функции:
* devices_list - список словарей с параметрами подключения к устройствам, которым надо передать команды
* config_commands - список команд, которые надо выполнить

Функция должна проверять результат на такие ошибки:
* Invalid input detected, Incomplete command, Ambiguous command

Если при выполнении какой-то из команд возникла ошибка, функция должна выводить сообщение
на стандартный поток вывода с информацией о том, какая ошибка возникла, при выполнении какой команды и на каком устройстве.

После обнаружения ошибки, функция должна спросить пользователя надо ли выполнять эту команду на других устройствах.

Варианты ответа [y]/n:
* y - выполнять команду на оставшихся устройствах (значение по умолчанию)
* n - не выполнять команду на оставшихся устройствах

Функция send_cfg_to_devices должна возвращать кортеж из двух словарей:
* первый словарь с выводом команд, которые выполнились без ошибки
* второй словарь с выводом команд, которые выполнились с ошибками

Оба словаря в формате
* ключ - IP устройства
* значение - вложенный словарь:
  * ключ - команда
  * значение - вывод с выполнением команд

В файле задания заготовлены команды с ошибками и без:
'''

import netmiko
from netmiko import ConnectHandler
import yaml
from pprint import pprint

with open('devices.yaml') as f:
    devices = yaml.safe_load(f)

device_list = []
bad_dict = {}
good_dict = {}
commands_with_errors = ['show ip int br', 'show run' ]
correct_commands = ['interface',
            'export compact']
commands = commands_with_errors + correct_commands

def send_cfg_to_devices(dev_list, com_list):
    ip_dict_bad = {}
    ip_dict_good = {}
    good_result_dict = {}
    bad_result_dict = {}
    i=0
    for dev in dev_list:
        i+=1
        with ConnectHandler(**dev) as ssh:
            ssh.enable()
            for command in com_list:
                result = ssh.send_command(command)
                if 'bad command' in result:
                    answer = input('The command {} on device {} is bad.'
                                   'Result is \n***{}\n***'
                                   'Proceed? Enter [y/n]'.format(command, dev['ip'], result))
                    if answer=='n':
                        print('You choose stop the program. The function will return empty dictionaries.')
                        break
                    else:
                        key1 = command
                        ip_dict_bad[key1] = result

                else:
                    key1 = command
                    ip_dict_good[key1] = result
            key2 = dev['ip']+'***'+str(i)
            if ip_dict_bad:
                bad_result_dict[key2] = ip_dict_bad
            if ip_dict_good:
                good_result_dict[key2] = ip_dict_good


    return bad_result_dict, good_result_dict


for device in devices['routers']:
    device_list.append(device)
try:
        bad_dict, good_dict = send_cfg_to_devices(device_list, commands)
        pprint(bad_dict)
        pprint("*****")
        pprint(good_dict)
except netmiko.ssh_exception.NetMikoAuthenticationException:
    print("Login or pass are not valid. Please check login/pass.")
except netmiko.ssh_exception.NetMikoTimeoutException:
    print("Connection to device {} timed-out".format(device['ip']))

