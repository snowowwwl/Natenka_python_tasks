# -*- coding: utf-8 -*-
"""
Задание 5.1

Запросить у пользователя ввод IP-сети в формате: 10.1.1.0/24

Затем вывести информацию о сети и маске в таком формате:

Network:
10        1         1         0
00001010  00000001  00000001  00000000

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
IP_list_int = [int(ip) for ip in IP_list]

ones=int(MASK)//8
ones_nulls = int(MASK)%8
MASK_bin = ('1'*8+'.')*ones +('1'*ones_nulls) + ('0'*(8-ones_nulls)) + '.' +('0'*8+'.')*(3-ones)
MASK_bin_list = MASK_bin.rstrip('.').split('.')

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

print(ip_template.format(IP_list_int[0], IP_list_int[1], IP_list_int[2], IP_list_int[3]))
print(m_t.format(MASK, int(MASK_bin_list[0],2), int(MASK_bin_list[1], 2), int(MASK_bin_list[2], 2), int(MASK_bin_list[3], 2)))
