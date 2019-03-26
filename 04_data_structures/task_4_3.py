# -*- coding: utf-8 -*-
"""
Задание 4.3

Получить из строки CONFIG список VLANов вида:
['1', '3', '10', '20', '30', '100']

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

CONFIG = 'switchport trunk allowed vlan 1,3,10,20,30,100'
CONFIG_list = CONFIG.split()
vlans = CONFIG_list[-1].split(',')
print(vlans)
