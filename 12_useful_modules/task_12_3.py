# -*- coding: utf-8 -*-
"""
Задание 12.3


Создать функцию ip_table, которая отображает таблицу доступных и недоступных IP-адресов.

Функция ожидает как аргументы два списка:
* список доступных IP-адресов
* список недоступных IP-адресов

Результат работы функции - вывод на стандартный поток вывода таблицы вида:

Reachable    Unreachable
-----------  -------------
10.1.1.1     10.1.1.7
10.1.1.2     10.1.1.8
             10.1.1.9

Функция не должна изменять списки, которые передавны ей как аргументы.
То есть, до выполнения функции и после списки должны выглядеть одинаково.

"""

from pprint import pprint
import ipaddress
from task_12_2 import check_ip_availability
from tabulate import tabulate
iplist = ['8.8.8.8-8.8.8.9', '8.8.8.10-8.8.8.11']


def ip_table(rulist):
    columns = ['Reachable', 'Unreachable']
    ru_dict = {key: [] for key in columns}
    ru_dict['Reachable'].append('\n'.join(rulist[0]))
    ru_dict['Unreachable'].append('\n'.join(rulist[1]))
    return tabulate(ru_dict, headers='keys')

print(ip_table(check_ip_availability(iplist)))
