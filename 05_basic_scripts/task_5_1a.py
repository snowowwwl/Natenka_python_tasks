# -*- coding: utf-8 -*-
"""
Задание 5.1a

Всё, как в задании 5.1. Но, если пользователь ввел адрес хоста, а не адрес сети,
то надо адрес хоста преобразовать в адрес сети и вывести адрес сети и маску, как в задании 5.1.

Пример адреса сети (все биты хостовой части равны нулю):
* 10.0.1.0/24
* 190.1.0.0/16

Пример адреса хоста:
* 10.0.1.1/24 - хост из сети 10.0.1.0/24
* 10.0.5.1/30 - хост из сети 10.0.5.0/30

Если пользователь ввел адрес 10.0.1.1/24,
вывод должен быть таким:

Network:
10        0         1         0
00001010  00000000  00000001  00000000

Mask:
/24
255       255       255       0
11111111  11111111  11111111  00000000

Проверить работу скрипта на разных комбинациях сеть/маска.

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

IPMASK = input('Enter ip address and mask in format x.x.x.x/y: ')
IP = IPMASK.split('/')[0]
MASK = IPMASK.split('/')[1]

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
