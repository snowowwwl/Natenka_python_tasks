# -*- coding: utf-8 -*-
"""
Задание 15.4

Создать функцию parse_sh_ip_int_br, которая ожидает как аргумент
имя файла, в котором находится вывод команды show

Функция должна обрабатывать вывод команды show ip int br и возвращать такие поля:
* Interface
* IP-Address
* Status
* Protocol

Информация должна возвращаться в виде списка кортежей:
[('FastEthernet0/0', '10.0.1.1', 'up', 'up'),
 ('FastEthernet0/1', '10.0.2.1', 'up', 'up'),
 ('FastEthernet0/2', 'unassigned', 'up', 'up')]

Для получения такого результата, используйте регулярные выражения.

Проверить работу функции на примере файла sh_ip_int_br_2.txt.

"""
import re
from pprint import pprint


def parse_sh_ip_int_br(filename):
    """
    Function takes information from the output of command "show ip interface brief"
    and return list of tuples like:
    [('FastEthernet0/0', '10.0.1.1', 'up', 'up'),
     ('FastEthernet0/1', '10.0.2.1', 'up', 'up'),
     ('FastEthernet0/2', 'unassigned', 'up', 'up')]
    :param filename:
    :return: list of tuples
    """
    regexpip = '(\S+) +(\d+\.\d+\.\d+\.\d+) +\S+ +\S+ +(\S+) +(\S+)\s+'
    with open(filename) as f:
        int_list = re.findall(regexpip, f.read())
    return int_list

if __name__ == "__main__":
    pprint(parse_sh_ip_int_br('sh_ip_int_br_2.txt'))
