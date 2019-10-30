# -*- coding: utf-8 -*-
"""
Задание 22.1a

Создать функцию parse_output_to_dict.

Параметры функции:
* template - имя файла, в котором находится шаблон TextFSM
* command_output - вывод соответствующей команды show (строка)

Функция должна возвращать список словарей:
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на выводе команды output/sh_ip_int_br.txt и шаблоне templates/sh_ip_int_br.template.
"""

import textfsm
from pprint import pprint


def parse_output_to_dict(template_file, command_output):
    with open(template_file) as template:
        fsm = textfsm.TextFSM(template)
    with open(command_output) as f:
        command = f.read()
        result = fsm.ParseText(command)
    result_list = []
    for line in result:
        line_dict = {fsm.header[i]:line[i] for i in range(len(line))}
        result_list.append(line_dict)
    return result_list

pprint(parse_output_to_dict('templates/sh_ip_int_br.template',
                            'output/sh_ip_int_br.txt'))

