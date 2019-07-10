# -*- coding: utf-8 -*-
"""
Задание 17.2

Создать функцию parse_sh_cdp_neighbors, которая обрабатывает
вывод команды show cdp neighbors.

Функция ожидает, как аргумент, вывод команды одной строкой (не имя файла).
Функция должна возвращать словарь, который описывает соединения между устройствами.

Например, если как аргумент был передан такой вывод:
R4>show cdp neighbors

Device ID    Local Intrfce   Holdtme     Capability       Platform    Port ID
R5           Fa 0/1          122           R S I           2811       Fa 0/1
R6           Fa 0/2          143           R S I           2811       Fa 0/0

Функция должна вернуть такой словарь:
{'R4': {'Fa0/1': {'R5': 'Fa0/1'},
        'Fa0/2': {'R6': 'Fa0/0'}}}

При этом интерфейсы могут быть записаны с пробелом Fa 0/0 или без Fa0/0.


Проверить работу функции на содержимом файла sh_cdp_n_sw1.txt
"""
import re
from pprint import pprint

def parse_sh_cdp_neighbors(shcdpne):
    final_dict = {}
    int_ne_dict = {}
    shcdpne_list = shcdpne.split('\n')
    for line in shcdpne_list:
        hostname = re.match('.+>',line)
        x = re.match('(\w+) +(.+?) +\d+ +\w \w \w +\d+ +(.+)', line)
        if x:
            ne_dict = {}
            ne_dict[x.group(1)] = x.group(3)
            int_ne_dict[x.group(2)] = ne_dict
        if hostname:
            final_dict[hostname.group().strip('>')] = int_ne_dict
    return final_dict


with open('sh_cdp_n_sw1.txt') as f:
    pprint(parse_sh_cdp_neighbors(f.read()))
