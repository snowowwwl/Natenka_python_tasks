# -*- coding: utf-8 -*-
"""
Задание 4.4

Из строк command1 и command2 получить список VLANов,
которые есть и в команде command1 и в команде command2.

Для данного примера, результатом должен быть список: [1, 3, 100]
Этот список содержит подсказку по типу итоговых данных.

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

command1 = 'switchport trunk allowed vlan 1,3,10,20,30,100'
command2 = 'switchport trunk allowed vlan 1,3,100,200,300'
command1_list = command1.split()
command2_list = command2.split()
vlan1 = command1_list[-1].split(',')
vlan2 = command2_list[-1].split(',')
intersection_vlan = set(vlan1).intersection(set(vlan2))
list_str = list(intersection_vlan)
list2 = sorted([int(list_str[i])for i in range(len(list_str))])
print(list2)




