# -*- coding: utf-8 -*-
"""
Задание 7.1

Аналогично заданию 4.6 обработать строки из файла ospf.txt
и вывести информацию по каждой в таком виде:
Protocol:              OSPF
Prefix:                10.0.24.0/24
AD/Metric:             110/41
Next-Hop:              10.0.13.3
Last update:           3d18h
Outbound Interface:    FastEthernet0/0

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""
ospf_route_keys = ['Protocol:', 'Prefix:', 'AD/Metric:', 'Next-Hop:', 'Last update:', 'Outbound Interface:']
with open('ospf.txt', 'r') as f:
    for line in f:
        ospf_route_list = line.split()
        ospf_route_list.remove('via')
        if ospf_route_list[0] == 'O':
            ospf_route_list[0] = 'OSPF'
        ospf_route_list = [i.strip(',') for i in ospf_route_list]
        print('#'*40)
        for i in range(len(ospf_route_list)):
            print('{:25}''{:25}'.format(ospf_route_keys[i], ospf_route_list[i]))
