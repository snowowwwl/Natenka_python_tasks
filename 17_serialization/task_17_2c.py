# -*- coding: utf-8 -*-
"""
Задание 17.2c

С помощью функции draw_topology из файла draw_network_graph.py
сгенерировать топологию, которая соответствует описанию в файле topology.yaml

Обратите внимание на то, какой формат данных ожидает функция draw_topology.
Описание топологии из файла topology.yaml нужно преобразовать соответствующим образом,
чтобы использовать функцию draw_topology.

Для решения задания можно создать любые вспомогательные функции.

Не копировать код функции draw_topology.

В итоге, должно быть сгенерировано изображение топологии.
Результат должен выглядеть так же, как схема в файле task_10_2c_topology.svg

При этом:
* Интерфейсы могут быть записаны с пробелом Fa 0/0 или без Fa0/0.
* Расположение устройств на схеме может быть другим
* Соединения должны соответствовать схеме


> Для выполнения этого задания, должен быть установлен graphviz:
> apt-get install graphviz

> И модуль python для работы с graphviz:
> pip install graphviz

"""
import os
from pprint import pprint
from draw_network_graph import draw_topology
import yaml
import re
import glob
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'


def parse_sh_cdp_neighbors_type2(shcdpne):
    final_dict = {}
    shcdpne_list = shcdpne.split('\n')
    for line in shcdpne_list:
        hostname = re.match('.+>', line)
        x = re.match('(\w+) +(.+?) +\d+ +\w \w \w? +.+? +(.+)', line)
        if hostname:
            k = hostname.group().strip('>')
        if x:
            ne_tuple = (x.group(1), x.group(3))
            lh_tuple = (k, x.group(2))
            final_dict[lh_tuple] = ne_tuple
    return final_dict

def generate_topology_from_cd(list_of_files, save_to_file=True, topology_filename='topology.yaml'):
    topology = {}
    for filename in list_of_files:
        with open(filename) as f:
            topology.update(parse_sh_cdp_neighbors_type2(f.read()))
    for key in list(topology):
        if topology[key] in topology.keys():
            del (topology[key])
    topology_dict = topology
    if save_to_file:
        with open(topology_filename, 'w') as f:
            yaml.dump(topology_dict, f, default_flow_style=False)
    return topology_dict


sh_version_files = glob.glob('sh_cdp_n_*')
pprint(generate_topology_from_cd(sh_version_files))

with open('topology.yaml') as f:
    topology = yaml.load(f.read())
    pprint(topology)
draw_topology(topology, out_filename='img/topology')