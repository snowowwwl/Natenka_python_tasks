# -*- coding: utf-8 -*-
"""
Задание 15.4a

Создать функцию convert_to_dict, которая ожидает два аргумента:
* список с названиями полей
* список кортежей с результатами отработки функции parse_sh_ip_int_br из задания 15.4

Функция возвращает результат в виде списка словарей (порядок полей может быть другой):
[{'interface': 'FastEthernet0/0', 'status': 'up', 'protocol': 'up', 'address': '10.0.1.1'},
 {'interface': 'FastEthernet0/1', 'status': 'up', 'protocol': 'up', 'address': '10.0.2.1'}]

Проверить работу функции на примере файла sh_ip_int_br_2.txt:
* первый аргумент - список headers
* второй аргумент - результат, который возвращает функции parse_show из прошлого задания.

Функцию parse_sh_ip_int_br не нужно копировать.
Надо импортировать или саму функцию, и использовать то же регулярное выражение,
что и в задании 15.4, или импортировать результат выполнения функции parse_show.

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""


from pprint import pprint
from task_15_4 import parse_sh_ip_int_br
headers = ['interface', 'address', 'status', 'protocol']


def convert_to_dict(list_of_headers, list_of_tuples):
    """
    Function takes list with keys and with parametres and returns a list of dict:
    [{'interface': 'FastEthernet0/0', 'status': 'up', 'protocol': 'up', 'address': '10.0.1.1'},
    {'interface': 'FastEthernet0/1', 'status': 'up', 'protocol': 'up', 'address': '10.0.2.1'}]
    :param list_of_headers:
    :param list_of_tuples:
    :return: dict
    """
    list_of_dict_ip = []
    for int_params in list_of_tuples:
        dict_ip = dict(zip(list_of_headers, int_params))
        list_of_dict_ip.append(dict_ip)
    return list_of_dict_ip


pprint(convert_to_dict(headers, parse_sh_ip_int_br('sh_ip_int_br_2.txt')))
