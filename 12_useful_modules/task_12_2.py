# -*- coding: utf-8 -*-
"""
Задание 12.2


Функция check_ip_addresses из задания 12.1 принимает только список адресов,
но было бы удобно иметь возможность указывать адреса с помощью диапазона, например,
192.168.100.1-10.

Создать функцию check_ip_availability, которая проверяет доступность IP-адресов.

Функция ожидает как аргумент список IP-адресов.

IP-адреса могут быть в формате:
* 10.1.1.1
* 10.1.1.1-10.1.1.10
* 10.1.1.1-10

Если адрес указан в виде диапазона, надо проверить доступность всех адресов диапазон
а включая последний.

Для упрощения задачи, можно считать, что в диапазоне всегда меняется только последни
й октет адреса.

Функция возвращает два списка:
* список доступных IP-адресов
* список недоступных IP-адресов


Для выполнения задачи можно воспользоваться функцией check_ip_addresses из задания 12.1
"""

from task_12_1 import check_ip_addresses
from pprint import pprint
import ipaddress


iplist = ['8.8.8.8-8.8.8.9', '192.168.1.1-192.168.1.3', '10.10.1.1']


def check_ip_availability(list_of_ip):
    print("Please waiting...")
    rangeiplist = []
    for ip in list_of_ip:
        if '-' in ip:
            first = ip.split('-')[0]
            last = ip.split('-')[1]
            firstip = ipaddress.ip_address(first)
            rangeip = int(last.split('.')[3]) - int(first.split('.')[3])+1
            for i in range(rangeip):
                rangeiplist.append(str(firstip + i))
        else:
            rangeiplist.append(ip)
    return check_ip_addresses(rangeiplist)

if __name__ == "__main__":
    pprint(check_ip_availability(iplist))
