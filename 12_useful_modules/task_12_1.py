# -*- coding: utf-8 -*-
"""
Задание 12.1

Создать функцию check_ip_addresses, которая проверяет доступность IP-адресов.

Функция ожидает как аргумент список IP-адресов.
И возвращает два списка:
* список доступных IP-адресов
* список недоступных IP-адресов

Для проверки доступности IP-адреса, используйте ping.
Адрес считается доступным, если на три ICMP-запроса пришли три ответа.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""

from pprint import pprint
import subprocess
import codecs
def check_ip_addresses(list_of_ip):
    """
        Ping list of IP address and return two lists of ip addresses -
        reachable and unreachable.
    """
    reach_iplist = []
    unreach_iplist = []
    for ip_address in list_of_ip:
        reply = subprocess.run(['ping', ip_address, '-n', '3'],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           encoding = 'ascii'
                               )
        if reply.returncode == 0:
            ###pprint(reply.stdout)
            reach_iplist.append(ip_address)
        else:
            unreach_iplist.append(ip_address)

    return reach_iplist, unreach_iplist


iplist = ['8.8.8.8', '192.168.1.1', '5.5.5.5', '10.10.10.10', '255.255.255.255', 'a']
print(check_ip_addresses(iplist))

