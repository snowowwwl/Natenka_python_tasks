# -*- coding: utf-8 -*-
'''
Задание 22.4

Создать функцию send_and_parse_show_command.

Параметры функции:
* device_dict - словарь с параметрами подключения к одному устройству
* command - команда, которую надо выполнить
* templates_path - путь к каталогу с шаблонами TextFSM
* index - имя индекс файла, значение по умолчанию "index"

Функция должна подключаться к одному устройству, отправлять команду show с помощью netmiko,
а затем парсить вывод команды с помощью TextFSM.

Функция должна возвращать список словарей с результатами обработки вывода команды (как в задании 22.1a):
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на примере вывода команды sh ip int br и устройствах из devices.yaml.
'''
import textfsm
from pprint import pprint
from task_22_1a import parse_output_to_dict
from netmiko import ConnectHandler
import yaml

def send_and_parse_show_command(device_dict, command, template_file):
    result_dict = {}
    with ConnectHandler(**device_dict) as ssh:
        ssh.enable()
        result = ssh.send_command(command)
    return parse_output_to_dict(template_file,result)

with open('devices.yaml') as f:
    devices = yaml.safe_load(f)
pprint(devices)
command = 'interface'
for device in devices:
    print(send_and_parse_show_command(device, command, 'templates/sh_ip_int_br.template'))


