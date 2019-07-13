# -*- coding: utf-8 -*-
"""
Задание 17.2a

С помощью функции parse_sh_cdp_neighbors из задания 17.2,
обработать вывод команды sh cdp neighbor из файлов:
* sh_cdp_n_sw1.txt
* sh_cdp_n_r1.txt
* sh_cdp_n_r2.txt
* sh_cdp_n_r3.txt
* sh_cdp_n_r4.txt
* sh_cdp_n_r5.txt
* sh_cdp_n_r6.txt

Объединить все словари, которые возвращает функция parse_sh_cdp_neighbors,
в один словарь topology и записать его содержимое в файл topology.yaml.

Структура словаря topology должна быть такой:
{'R4': {'Fa0/1': {'R5': 'Fa0/1'},
        'Fa0/2': {'R6': 'Fa0/0'}},
 'R5': {'Fa0/1': {'R4': 'Fa0/1'}},
 'R6': {'Fa0/0': {'R4': 'Fa0/2'}}}

При этом интерфейсы могут быть записаны с пробелом Fa 0/0 или без Fa0/0.

Не копировать код функции parse_sh_cdp_neighbors
"""


from pprint import pprint
import glob
from task_17_2 import parse_sh_cdp_neighbors
import yaml

sh_version_files = glob.glob('sh_cdp_n_*')
topology = {}
for filename in sh_version_files:
    with open(filename) as f:
        topology.update(parse_sh_cdp_neighbors(f.read()))

pprint(topology)
with open('topology.yaml', 'w') as f:
    yaml.dump(topology, f, default_flow_style=False)
print('++++++++++++++')
with open('topology.yaml') as f:
    print(f.read())
