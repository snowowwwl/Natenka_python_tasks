# -*- coding: utf-8 -*-
"""
Задание 22.3

Создать функцию parse_command_dynamic.

Параметры функции:
* command_output - вывод команды (строка)
* attributes_dict - словарь атрибутов, в котором находятся такие пары ключ-значение:
 * 'Command': команда
 * 'Vendor': вендор
* index_file - имя файла, где хранится соответствие между командами и шаблонами. Значение по умолчанию - "index"
* templ_path - каталог, где хранятся шаблоны. Значение по умолчанию - templates

Функция должна возвращать список словарей с результатами обработки вывода команды (как в задании 22.1a):
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на примере вывода команды sh ip int br.
"""

##############
#Not supported on windows(
##############


import textfsm
from pprint import pprint
from task_22_1a import parse_output_to_dict
from textfsm import clitable

def parse_command_dynamic(command_output, attributes_dict, index_file = 'index', templ_path = 'templates'):
    cli_table = clitable.CliTable(index_file, templ_path)
    cli_table.ParseCmd(command_output, attributes_dict)
    print('Formatted Table:\n', cli_table.FormattedTable())
    result_list = []
    header = list(cli_table.header)
    for line in cli_table:
        line_dict = {header[i]: line[i] for i in range(len(line))}
        result_list.append(line_dict)
    return result_list





output_sh_ip_int_br = open('output/sh_ip_int_br.txt').read()
attributes = {'Command': 'show ip int br' , 'Vendor': 'Cisco'}
pprint(parse_command_dynamic(output_sh_ip_int_br, attributes))




