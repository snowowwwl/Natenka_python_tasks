# -*- coding: utf-8 -*-
"""
Задание 9.3

Создать функцию get_int_vlan_map, которая обрабатывает конфигурационный файл коммутатора
и возвращает два объекта:
* словарь портов в режиме access, где ключи номера портов, а значения access VLAN:
{'FastEthernet0/12':10,
 'FastEthernet0/14':11,
 'FastEthernet0/16':17}

* словарь портов в режиме trunk, где ключи номера портов, а значения список разрешенных VLAN:
{'FastEthernet0/1':[10,20],
 'FastEthernet0/2':[11,30],
 'FastEthernet0/4':[17]}

Функция ожидает в качестве аргумента имя конфигурационного файла.

Проверить работу функции на примере файла config_sw1.txt


Ограничение: Все задания надо выполнять используя только пройденные темы.
"""


def get_int_vlan_map(file):
    """
    This function reads configuration file and returns the dictionary of ports
    with vlan numbers as a value
    :param file: name of file
    :return: dictionary of ports : 'FastEthernet0/1':[10,20]
    """
    port_dict = {}
    port = str()
    with open(file, 'r') as f:
        for line in f:
            if 'interface' in line:
                port = line.lstrip('interface ').rstrip('\n')
            elif 'access vlan' in line:
                port_dict[port] = line.split()[-1]
            elif 'trunk allowed vlan' in line:
                vlans = line.split()[-1].split(',')
                port_dict[port] = vlans
    return port_dict


print(get_int_vlan_map('C:/Users/snowowl/PycharmProjects/Natenka_python_tasks/09_functions/config_sw1.txt'))
