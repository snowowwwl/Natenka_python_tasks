# -*- coding: utf-8 -*-
"""
Задание 11.2

С помощью функции parse_cdp_neighbors из задания 11.1
и функции draw_topology из файла draw_network_graph.py
сгенерировать топологию, которая соответствует выводу
команды sh cdp neighbor в файле sw1_sh_cdp_neighbors.txt

Не копировать код функций parse_cdp_neighbors и draw_topology.

В итоге, должен быть сгенерировано изображение топологии.
Результат должен выглядеть так же, как схема в файле task_11_2_topology.svg

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

import sys
sys.path.insert(0, 'C:/Users/snowowl/PycharmProjects/Natenka_python_tasks/11_modules/')
from draw_network_graph import draw_topology
from task_11_1 import parse_cdp_neighbors
import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'

with open('C:/Users/snowowl/PycharmProjects/Natenka_python_tasks/11_modules/sw1_sh_cdp_neighbors.txt', 'r') as f:
    showcdpne = f.read()
draw_topology(parse_cdp_neighbors(showcdpne), output_filename='img/topology')