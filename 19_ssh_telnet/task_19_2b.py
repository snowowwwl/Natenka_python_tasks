# -*- coding: utf-8 -*-
'''
Задание 19.2b

В этом задании необходимо переделать функцию send_config_commands из задания 19.2a или 19.2 и добавить проверку на ошибки.

При выполнении каждой команды, скрипт должен проверять результат на такие ошибки:
 * Invalid input detected, Incomplete command, Ambiguous command

Если при выполнении какой-то из команд возникла ошибка,
функция должна выводить сообщение на стандартный поток вывода с информацией
о том, какая ошибка возникла, при выполнении какой команды и на каком устройстве.

При этом, параметр verbose также должен работать, но теперь он отвечает за вывод
только тех команд, которые выполнились корректно.

Функция send_config_commands теперь должна возвращать кортеж из двух словарей:
* первый словарь с выводом команд, которые выполнились без ошибки
* второй словарь с выводом команд, которые выполнились с ошибками

Оба словаря в формате:
* ключ - команда
* значение - вывод с выполнением команд

Отправить список команд commands на все устройства из файла devices.yaml (для этого надо считать информацию из файла) с помощью функции send_config_commands.

Примеры команд с ошибками:
R1(config)#logging 0255.255.1
                   ^
% Invalid input detected at '^' marker.

R1(config)#logging
% Incomplete command.

R1(config)#i
% Ambiguous command:  "i"

В файле задания заготовлены команды с ошибками и без:
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
        bad_dict, good_dict = send_show_command(device, commands, 'no')
        pprint(bad_dict)
        pprint("*****")
        pprint(good_dict)
except netmiko.ssh_exception.NetMikoAuthenticationException:
    print("Login or pass are not valid. Please check login/pass.")
except netmiko.ssh_exception.NetMikoTimeoutException:
    print("Connection to device {} timed-out".format(device['ip']))
