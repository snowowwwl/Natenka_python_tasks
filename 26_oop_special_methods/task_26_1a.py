# -*- coding: utf-8 -*-

'''
Задание 26.1a

В этом задании надо сделать так, чтобы экземпляры класса Topology были итерируемыми объектами.
Основу класса Topology можно взять из любого задания 25.1x или задания 26.1.

После создания экземпляра класса, экземпляр должен работать как итерируемый объект.
На каждой итерации должен возвращаться кортеж, который описывает одно соединение.
Порядок вывода соединений может быть любым.


Пример работы класса:

In [1]: top = Topology(topology_example)

In [2]: for link in top:
   ...:     print(link)
   ...:
(('R1', 'Eth0/0'), ('SW1', 'Eth0/1'))
(('R2', 'Eth0/0'), ('SW1', 'Eth0/2'))
(('R2', 'Eth0/1'), ('SW2', 'Eth0/11'))
(('R3', 'Eth0/0'), ('SW1', 'Eth0/3'))
(('R3', 'Eth0/1'), ('R4', 'Eth0/0'))
(('R3', 'Eth0/2'), ('R5', 'Eth0/0'))


Проверить работу класса.
'''

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

    def __add__(self, other):
        topology = {}
        newtopo = Topology(topology)
        newtopo.topology.update(self.topology)
        newtopo.topology.update(other.topology)
        return newtopo

    def __iter__(self):
        print('__ITERATION__')
        return iter(self.topology.items())


top = Topology(topology_example)
for link in top:
    print(link)
