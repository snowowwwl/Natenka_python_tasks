# -*- coding: utf-8 -*-
"""
Задание 7.3a

Сделать копию скрипта задания 7.3.

Дополнить скрипт:
- Отсортировать вывод по номеру VLAN


Ограничение: Все задания надо выполнять используя только пройденные темы.

"""


with open('CAM_table.txt', 'r') as src, open('CAM_table_new.txt', 'w') as dst:
    lines_list=[]
    for line in src:
        if line.count('.') == 2:
            lines_list.append(line)
    lines_list.sort()
    dst.writelines(lines_list)
with open('CAM_table_new.txt', 'r') as f:
    for line in f:
        if line.count('.') == 2:
            line_list = line.split()
            line_list.pop(2)
            vlan, mac, intf = [i for i in line_list]
            print("{:10} {:20} {:10}".format(vlan, mac, intf))


