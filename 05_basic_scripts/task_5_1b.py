# -*- coding: utf-8 -*-
"""
Задание 5.1b

Преобразовать скрипт из задания 5.1a таким образом,
чтобы сеть/маска не запрашивались у пользователя,
а передавались как аргумент скрипту.

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""


from sys import argv
IP, MASK = argv[1:]
print('*'*30)
print(IP, '/', MASK)

IP_list = IP.split('.')
IP_bin = [bin(int(ip))[2:].zfill(8) for ip in IP_list]

ones=int(MASK)//8
ones_nulls = int(MASK)%8
MASK_bin = ('1'*8+'.')*ones +('1'*ones_nulls) + ('0'*(8-ones_nulls)) + '.' +('0'*8+'.')*(3-ones)
MASK_bin_list = MASK_bin.rstrip('.').split('.')

NET = [int(IP_bin[i], 2) & int(MASK_bin_list[i], 2) for i in range(4)]

ip_template = '''
Network:
{0:<8} {1:<8} {2:<8} {3:<8}
{0:08b} {1:08b} {2:08b} {3:08b}

'''

m_t = '''
Mask:
/{0:}
{1:<8} {2:<8} {3:<8} {4:<8}
{1:08b} {2:08b} {3:08b} {4:08b}

'''

print(ip_template.format(NET[0], NET[1], NET[2], NET[3]))
print(m_t.format(MASK, int(MASK_bin_list[0],2), int(MASK_bin_list[1], 2), int(MASK_bin_list[2], 2), int(MASK_bin_list[3], 2)))
