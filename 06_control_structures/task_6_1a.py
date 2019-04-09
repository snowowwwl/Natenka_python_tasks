# -*- coding: utf-8 -*-
"""
Задание 6.1a

Сделать копию скрипта задания 6.1.

Дополнить скрипт:
- Добавить проверку введенного IP-адреса.
- Адрес считается корректно заданным, если он:
   - состоит из 4 чисел разделенных точкой,
   - каждое число в диапазоне от 0 до 255.

Если адрес задан неправильно, выводить сообщение:
'Incorrect IPv4 address'

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""


IP = input("Enter IP adress in format x.x.x.x : ")
IP_list = IP.split('.')

for i in IP_list:
    if not(i.isdigit()):
        print("Incorrect IP address")
        break
    if int(i) > 255:
        print("Incorrect IP address")
        break
    if len(IP_list) != 4:
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
