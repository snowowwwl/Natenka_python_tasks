# -*- coding: utf-8 -*-
'''
Задание 15.3a

Переделать функцию parse_cfg из задания 15.3 таким образом, чтобы она возвращала словарь:
* ключ: имя интерфейса
* значение: кортеж с двумя строками:
  * IP-адрес
  * маска

Например (взяты произвольные адреса):
{'FastEthernet0/1':('10.0.1.1', '255.255.255.0'),
 'FastEthernet0/2':('10.0.2.1', '255.255.255.0')}

Для получения такого результата, используйте регулярные выражения.

Проверить работу функции на примере файла config_r1.txt.

Обратите внимание, что в данном случае, можно не проверять корректность IP-адреса,
диапазоны адресов и так далее, так как обрабатывается вывод команды, а не ввод пользователя.

'''

import re

from pprint import pprint


def parse_cfg(filename):
    # return ip/mask in dict :
    # {'FastEthernet0/1':('10.0.1.1', '255.255.255.0'),
    #  'FastEthernet0/2':('10.0.2.1', '255.255.255.0')}#
    regexpip = 'ip address (\d+\.\d+\.\d+\.\d+) (\d+\.\d+\.\d+\.\d+)'
    regexpint ='interface (\w+)\s+ .+\s? .+' ### \w+\s+ ip address '
    with open(filename) as f:
        s = f.read()
        ipmasklist = re.findall(regexpip, s)
        ###interfaces = re.findall(r'interface (.+)\n\s+ip address|interface (.+)\n\s+.+\n\s+ip address'
                                ###'|interface (.+)\n\s+.+\n\s+.+\n\s+ip address', s)
        interfaces = re.findall(r'interface (.+)\n\s+(?:.+\n\s+){0,2}ip address',s)
        int_dict = dict(zip(interfaces,ipmasklist))
        print(ipmasklist)
        print(interfaces)
    return int_dict


pprint(parse_cfg('config_r1.txt'))
