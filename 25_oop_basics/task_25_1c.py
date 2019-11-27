# -*- coding: utf-8 -*-

'''
Задание 25.1c

Изменить класс Topology из задания 25.1b.

Добавить метод delete_node, который удаляет все соединения с указаным устройством.

Если такого устройства нет, выводится сообщение "Такого устройства нет".

Создание топологии
In [1]: t = Topology(topology_example)

In [2]: t.topology
Out[2]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Удаление устройства:
In [3]: t.delete_node('SW1')

In [4]: t.topology
Out[4]:
{('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Если такого устройства нет, выводится сообщение:
In [5]: t.delete_node('SW1')
Такого устройства нет

'''
from pprint import pprint
topology_example = {('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
                    ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
                    ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
                    ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
                    ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
                    ('R3', 'Eth0/2'): ('R5', 'Eth0/0'),
                    ('SW1', 'Eth0/1'): ('R1', 'Eth0/0'),
                    ('SW1', 'Eth0/2'): ('R2', 'Eth0/0'),
                    ('SW1', 'Eth0/3'): ('R3', 'Eth0/0')}


class Topology:

    def _normalize(self, topology_dict):
        topology = {}
        topology.update(topology_dict)
        for key in topology_dict:
            if topology.get(topology_dict[key]) is None:
                pass
            else:
                if topology.get(key):
                    del (topology[topology_dict[key]])
        return topology

    def __init__(self, topology_dict):
        self.topology = self._normalize(topology_dict)

    def delete_link(self, right_side, left_side):
        if self.topology.get(right_side):
            if self.topology[right_side] == left_side:
                del (self.topology[right_side])
        elif self.topology.get(left_side):
            if self.topology[left_side] == right_side:
                del (self.topology[left_side])
        else:
            print("Such link is not exist")

    def delete_node(self, node):
        topology = {}
        topology.update(self.topology)
        delf = 0
        for key, value  in topology.items():
            if key[0] == node:
                del (self.topology[key])
                delf = 1
            elif value[0] == node:
                del (self.topology[key])
                delf = 1
        if delf == 0:
            print("Such node is not exist")



t = Topology(topology_example)
pprint(t.topology)
t.delete_node('SW1')
pprint(t.topology)
t.delete_node('SW1')
