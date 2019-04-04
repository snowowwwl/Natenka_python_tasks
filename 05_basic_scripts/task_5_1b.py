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
IP_list_int = [int(ip) for ip in IP_list]
IP_bin = []
for i in range(len(IP_list_int)):
    IP_bin.append(bin(IP_list_int[i])[2:].zfill(8))

MASK_bin = '1'*int(MASK) + '0'*(32 - int(MASK))
i = 0
MASK_bin_list = []
while(i < len(MASK_bin)):
    MASK_bin_list.append(MASK_bin[i:i+8])
    i += 8

NET = []
for i in range(len(IP_list_int)):
    NET.append(int(IP_bin[i], 2) & int(MASK_bin_list[i], 2))

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
print(m_t.format(MASK, int(MASK_bin[0:8], 2), int(MASK_bin[8:16], 2), int(MASK_bin[16:24], 2), int(MASK_bin[24:32], 2)))
