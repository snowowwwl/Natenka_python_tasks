# -*- coding: utf-8 -*-
"""
Задание 4.7

Преобразовать MAC-адрес в двоичную строку (без двоеточий).

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

MAC = 'AAAA:BBBB:CCCC'
MAC_LIST = list(MAC.split(':'))
MAC_str = ''.join(str(mac)for mac in MAC_LIST)
MAC_bin = str()
for i in range(len(MAC_str)):
    s = '0x'+MAC_str[i]
    MAC_bin += str(bin(int(s, 16))).lstrip('0b')
print(MAC_bin)
