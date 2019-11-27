# -*- coding: utf-8 -*-

'''
Задание 25.1d

Изменить класс Topology из задания 25.1c

Добавить метод add_link, который добавляет указанное соединение, если его еще нет в топологии
Если соединение существует, вывести сообщение "Такое соединение существует",
Если одна из сторон есть в топологии, вывести сообщение "Cоединение с одним из портов существует"


Создание топологии
In [7]: t = Topology(topology_example)

In [8]: t.topology
Out[8]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [9]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))

In [10]: t.topology
Out[10]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R1', 'Eth0/4'): ('R7', 'Eth0/0'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [11]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))
Такое соединение существует

In [12]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/5'))
Cоединение с одним из портов существует


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

    def add_link(self, left, right):
        if self.topology.get(left) == right:
            print("Such link is already exist")
        elif self.topology.get(left):
            print("Such left side is already connected")
        elif right in self.topology.values():
            print("Such right side is already connected")
        else:
            self.topology[left] = right

t = Topology(topology_example)
pprint(t.topology)
pprint("t.add_link('R1', 'Eth0/4'), ('R7', 'Eth0/0')")
t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))
pprint(t.topology)

pprint("t.add_link('R1', 'Eth0/4'), ('R7', 'Eth0/0')")
t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))
pprint(t.topology)

pprint("t.add_link('R1', 'Eth0/4'), ('R7', 'Eth0/5')")
t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/5'))
pprint(t.topology)


