# -*- coding: utf-8 -*-
"""
Задание 4.6

Обработать строку ospf_route и вывести информацию в виде:
Protocol:              OSPF
Prefix:                10.0.24.0/24
AD/Metric:             110/41
Next-Hop:              10.0.13.3
Last update:           3d18h
Outbound Interface:    FastEthernet0/0

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

ospf_route = 'O        10.0.24.0/24 [110/41] via 10.0.13.3, 3d18h, FastEthernet0/0'
ospf_route_list = ospf_route.split()
ospf_route_list.remove('via')
for i in range(len(ospf_route_list)):
    ospf_route_list[i] = ospf_route_list[i].strip(',')
    if ospf_route_list[i] == 'O':
        ospf_route_list[i] = 'OSPF'

print(ospf_route_list)

ospf_route_keys = ['Protocol:', 'Prefix:', 'AD/Metric:', 'Next-Hop:', 'Last update:', 'Outbound Interface:']
for i in range(len(ospf_route_list)):
    print('{:25}''{:25}'.format(ospf_route_keys[i], ospf_route_list[i]))
