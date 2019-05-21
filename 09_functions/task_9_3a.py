# -*- coding: utf-8 -*-
"""
Задание 9.3a

Сделать копию скрипта задания 9.3.

Дополнить скрипт:
    - добавить поддержку конфигурации, когда настройка access-порта выглядит так:
            interface FastEthernet0/20
                switchport mode access
                duplex auto
      То есть, порт находится в VLAN 1

В таком случае, в словарь портов должна добавляться информация, что порт в VLAN 1
      Пример словаря: {'FastEthernet0/12':10,
                       'FastEthernet0/14':11,
                       'FastEthernet0/20':1 }

Функция ожидает в качестве аргумента имя конфигурационного файла.

Проверить работу функции на примере файла config_sw2.txt


Ограничение: Все задания надо выполнять используя только пройденные темы.
"""


def get_int_vlan_map(file):
    """
    This function reads configuration file and returns the dictionary of ports
    with vlan numbers as a value. If port is not configured, function will add such note in dictionary:
    'FastEthernet0/20':1
    :param file: name of file
    :return: dictionary of ports : 'FastEthernet0/1':[10,20]
    """
    port_dict = {}
    port = str()
    with open(file, 'r') as f:
        config_list = f.readlines()
        for i in range(len(config_list)-1):
            line = config_list[i]
            nline = config_list[i+1]
            if 'interface' in line:
                port = line.lstrip('interface ').rstrip('\n')
            elif 'trunk allowed vlan' in line:
                vlans = line.split()[-1].split(',')
                port_dict[port] = vlans
            elif 'switchport mode access' in line and 'access vlan' in nline:
                port_dict[port] = nline.split()[-1]
            elif 'switchport mode access' in line and 'access vlan' not in nline:
                port_dict[port] = '1'
    return port_dict


print(get_int_vlan_map('C:/Users/snowowl/PycharmProjects/Natenka_python_tasks/09_functions/config_sw2.txt'))
