# -*- coding: utf-8 -*-

'''
Задание 26.1

Изменить класс Topology из задания 25.1x.

Добавить метод, который позволит выполнять сложение двух объектов (экземпляров) Topology.
В результате сложения должен возвращаться новый экземпляр класса Topology.

Создание двух топологий:

In [1]: t1 = Topology(topology_example)

In [2]: t1.topology
Out[2]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [3]: topology_example2 = {('R1', 'Eth0/4'): ('R7', 'Eth0/0'),
                             ('R1', 'Eth0/6'): ('R9', 'Eth0/0')}

In [4]: t2 = Topology(topology_example2)

In [5]: t2.topology
Out[5]: {('R1', 'Eth0/4'): ('R7', 'Eth0/0'), ('R1', 'Eth0/6'): ('R9', 'Eth0/0')}

Суммирование топологий:

In [6]: t3 = t1+t2

In [7]: t3.topology
Out[7]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R1', 'Eth0/4'): ('R7', 'Eth0/0'),
 ('R1', 'Eth0/6'): ('R9', 'Eth0/0'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Проверка, что исходные топологии не изменились:

In [9]: t1.topology
Out[9]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [10]: t2.topology
Out[10]: {('R1', 'Eth0/4'): ('R7', 'Eth0/0'), ('R1', 'Eth0/6'): ('R9', 'Eth0/0')}
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

topology_example2 = {('R1', 'Eth0/4'): ('R7', 'Eth0/0'),
                     ('R1', 'Eth0/6'): ('R9', 'Eth0/0')}


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

    def add_link(self, left, right):
        if self.topology.get(left) == right:
            print("Such link is already exist")
        elif self.topology.get(left):
            print("Such left side is already connected")
        elif right in self.topology.values():
            print("Such right side is already connected")
        else:
            self.topology[left] = right

    def __add__(self, other):
        topology = {}
        newtopo = Topology(topology)
        newtopo.topology.update(self.topology)
        newtopo.topology.update(other.topology)
        return newtopo

t1 = Topology(topology_example)
pprint(t1.topology)
t2 = Topology(topology_example2)
pprint(t2.topology)
t3 = t1+t2
pprint(t3.topology)
pprint("t1")
pprint(t1.topology)
pprint("t2")
pprint(t2.topology)