# -*- coding: utf-8 -*-
"""
Задание 6.1b

Сделать копию скрипта задания 6.1a.

Дополнить скрипт:
Если адрес был введен неправильно, запросить адрес снова.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""

IP = input("Enter IP adress in format x.x.x.x : ")
IP_correct = False
while not IP_correct:
    IP_list = IP.split('.')
    for i in IP_list:
        if not(i.isdigit()):
            print("Incorrect IP address")
            IP = input("Enter IP adress again: ")
            break
        if int(i) > 255:
            print("Incorrect IP address")
            IP = input("Enter IP adress again: ")
            break
        if len(IP_list) != 4:
            print("Incorrect IP address")
            IP = input("Enter IP adress again: ")
            break
    else:
        IP_correct = True
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
