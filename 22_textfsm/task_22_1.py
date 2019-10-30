# -*- coding: utf-8 -*-
"""
Задание 22.1

Создать функцию parse_command_output. Параметры функции:
* template - имя файла, в котором находится шаблон TextFSM
* command_output - вывод соответствующей команды show (строка)

Функция должна возвращать список:
* первый элемент - это список с названиями столбцов
* остальные элементы это списки, в котором находятся результаты обработки вывода

Проверить работу функции на выводе команды output/sh_ip_int_br.txt и шаблоне templates/sh_ip_int_br.template.

"""

import textfsm
from pprint import pprint


def parse_command_output(template_file, command_output):
    with open(template_file) as template:
        fsm = textfsm.TextFSM(template)
    with open(command_output) as f:
        command = f.read()
        result = fsm.ParseText(command)
    result_list = []
    result_list.append((fsm.header))
    result_list.append(result)
    return result_list

pprint(parse_command_output('templates/sh_ip_int_br.template',
                            'output/sh_ip_int_br.txt'))



