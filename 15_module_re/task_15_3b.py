# -*- coding: utf-8 -*-
"""
Задание 15.3b

Проверить работу функции parse_cfg из задания 15.3a на конфигурации config_r2.txt.

Обратите внимание, что на интерфейсе e0/1 назначены два IP-адреса:
interface Ethernet0/1
 ip address 10.255.2.2 255.255.255.0
 ip address 10.254.2.2 255.255.255.0 secondary

А в словаре, который возвращает функция parse_cfg, интерфейсу Ethernet0/1
соответствует только один из них (второй).

Переделайте функцию parse_cfg из задания 15.3a таким образом,
чтобы она возвращала список кортежей для каждого интерфейса.
Если на интерфейсе назначен только один адрес, в списке будет один кортеж.
Если же на интерфейсе настроены несколько IP-адресов, то в списке будет несколько кортежей.

Проверьте функцию на конфигурации config_r2.txt и убедитесь, что интерфейсу
Ethernet0/1 соответствует список из двух кортежей.

Обратите внимание, что в данном случае, можно не проверять корректность IP-адреса,
диапазоны адресов и так далее, так как обрабатывается вывод команды, а не ввод пользователя.

"""
import re

from pprint import pprint


def parse_cfg(filename):
    # return ip/mask in dict :
    # {'FastEthernet0/1':('10.0.1.1', '255.255.255.0'),
    #  'FastEthernet0/2':('10.0.2.1', '255.255.255.0')}#
    regexpip = '(?:ip address (\d+\.\d+\.\d+\.\d+) (\d+\.\d+\.\d+\.\d+)\n){1,2}'
    with open(filename) as f:
        int_dict1={}
        s = f.read()
        s_list = re.split('!',s)
        for line in s_list:
            ipmasklist = re.findall(r'ip address (\d+\.\d+\.\d+\.\d+) (\d+\.\d+\.\d+\.\d+)', line)
            interfaces = re.findall(r'interface (.+)\n\s+(?:.+\n\s+){0,2}ip address',line)
            if interfaces:
                int_dict1[str(interfaces).strip('[]').strip("'")] = ipmasklist
    return int_dict1


pprint(parse_cfg('config_r2.txt'))