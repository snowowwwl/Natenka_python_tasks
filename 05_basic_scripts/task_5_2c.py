# -*- coding: utf-8 -*-
"""
Задание 5.2c

Переделать скрипт из задания 5.2b таким образом, чтобы, при запросе параметра,
которого нет в словаре устройства, отображалось сообщение 'Такого параметра нет'.

> Попробуйте набрать неправильное имя параметра или несуществующий параметр,
чтобы увидеть какой будет результат. А затем выполняйте задание.

Если выбран существующий параметр,
вывести информацию о соответствующем параметре, указанного устройства.

Пример выполнения скрипта:
$ python task_4_5c.py
Enter device name: r1
Enter parameter name (ios, model, vendor, location, ip): io
Такого параметра нет

Ограничение: нельзя изменять словарь london_co.

Все задания надо выполнять используя только пройденные темы.
То есть эту задачу можно решить без использования условия if.
"""

london_co = {
    'r1': {
        'location': '21 New Globe Walk',
        'vendor': 'Cisco',
        'model': '4451',
        'ios': '15.4',
        'ip': '10.255.0.1'
    },
    'r2': {
        'location': '21 New Globe Walk',
        'vendor': 'Cisco',
        'model': '4451',
        'ios': '15.4',
        'ip': '10.255.0.2'
    },
    'sw1': {
        'location': '21 New Globe Walk',
        'vendor': 'Cisco',
        'model': '3850',
        'ios': '3.6.XE',
        'ip': '10.255.0.101',
        'vlans': '10,20,30',
        'routing': True
    }
}

NAME = input("Enter device name(r1, r2 or sw1): ")
NAME_list = list((london_co[NAME].keys()))
NAME_str = ', '.join(NAME_list)

DETAIL = input("Enter what additional information you need ({}):".format(NAME_str))
print(london_co[NAME].get(DETAIL, "There is no such information"))
