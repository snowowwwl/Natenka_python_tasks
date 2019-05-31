# -*- coding: utf-8 -*-
"""
Задание 11.2a

С помощью функции parse_cdp_neighbors из задания 11.1
и функции draw_topology из файла draw_network_graph.py
сгенерировать топологию, которая соответствует выводу
команды sh cdp neighbor из файлов:
* sh_cdp_n_sw1.txt
* sh_cdp_n_r1.txt
* sh_cdp_n_r2.txt
* sh_cdp_n_r3.txt


Не копировать код функций parse_cdp_neighbors и draw_topology.

В итоге, должен быть сгенерировано изображение топологии.
Результат должен выглядеть так же, как схема в файле task_11_2a_topology.svg


При этом:
* Интерфейсы могут быть записаны с пробелом Fa 0/0 или без Fa0/0.
* Расположение устройств на схеме может быть другим
* Соединения должны соответствовать схеме

Ограничение: Все задания надо выполнять используя только пройденные темы.

> Для выполнения этого задания, должен быть установлен graphviz:
> apt-get install graphviz

> И модуль python для работы с graphviz:
> pip install graphviz

"""

import os
import sys
from draw_network_graph import draw_topology
from task_11_1 import parse_cdp_neighbors
from pprint import pprint
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'
sys.path.insert(0, 'C:/Users/snowowl/PycharmProjects/Natenka_python_tasks/11_modules/')

files = ['sh_cdp_n_sw1.txt', 'sh_cdp_n_r1.txt', 'sh_cdp_n_r2.txt', 'sh_cdp_n_r3.txt']

topology_dict = {}
topology_dict_temp = {}

for filename in files:
    with open('C:/Users/snowowl/PycharmProjects/Natenka_python_tasks/11_modules/' + filename, 'r') as f:
        showcdpne = f.read()
        topology_dict_temp = parse_cdp_neighbors(showcdpne)
        for key in topology_dict_temp:
            if topology_dict.get(topology_dict_temp[key]) is None:
                pass
            else:
                del(topology_dict[topology_dict_temp[key]])
            topology_dict.update(topology_dict_temp)
pprint(topology_dict)
draw_topology(topology_dict, output_filename='img/topology')
