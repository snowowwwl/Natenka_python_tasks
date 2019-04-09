# -*- coding: utf-8 -*-
"""
Задание 6.1

1. Запросить у пользователя ввод IP-адреса в формате 10.0.1.1
2. Определить какому классу принадлежит IP-адрес.
3. В зависимости от класса адреса, вывести на стандартный поток вывода:
   'unicast' - если IP-адрес принадлежит классу A, B или C
   'multicast' - если IP-адрес принадлежит классу D
   'local broadcast' - если IP-адрес равен 255.255.255.255
   'unassigned' - если IP-адрес равен 0.0.0.0
   'unused' - во всех остальных случаях

Подсказка по классам (диапазон значений первого байта в десятичном формате):
A: 1-127
B: 128-191
C: 192-223
D: 224-239

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""

IP = input("Enter IP adress in format x.x.x.x : ")
IP_list = IP.split('.')
for i in IP_list:
    if int(i) > 255:
        print("Incorrect IP address")
        break
else:
    if 1 <= int(IP_list[0]) <= 223:
        print("Unicast")
        if 1 <= int(IP_list[0]) <= 127:
            print("Class A")
        elif 128 <= int(IP_list[0]) <= 191:
            print("Class B")
        elif 192 <= int(IP_list[0]) <= 223:
            print("Class C")
        elif 224 <= int(IP_list[0]) <= 239:
            print("Multicast")
            print("Class D")
        elif IP == '255.255.255.255':
            print("Local broadcast")
        elif IP == '0.0.0.0':
            print("Unassigned")
    else:
        print("Unused")
