# -*- coding: utf-8 -*-
"""
Задание 20.1

Создать функцию ping_ip_addresses, которая проверяет доступность IP-адресов.
Проверка IP-адресов должна выполняться параллельно в разных потоках.

Параметры функции:
* ip_list - список IP-адресов
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для выполнения задания можно создавать любые дополнительные функции.

Для проверки доступности IP-адреса, используйте ping.
"""
import yaml
import subprocess
from concurrent.futures import ThreadPoolExecutor
import logging
from datetime import datetime

logging.basicConfig(
    format='%(threadName)s %(name)s %(levelname)s: %(message)s',
    level=logging.INFO)

def ping_ip(ip_address):
    """
    Ping IP address and return tuple:
    On success:
        * True
        * command output (stdout)
    On failure:
        * False
        * error output (stderr)
    """
    start_msg = '===> {} Connection: {}'
    received_msg = '<=== {} Received:   {} Error_code:{}'
    logging.info(start_msg.format(datetime.now().time(), ip_address))

    reply = subprocess.run(['ping', ip_address, '-n', '3'],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           encoding='ascii'
                           )
    if reply.returncode == 0:
        logging.info(received_msg.format(datetime.now().time(), ip_address, reply.returncode))
        return True
    else:
        logging.info(received_msg.format(datetime.now().time(), ip_address, reply.returncode))
        return False

def ping_ip_addresses(ip_list, limit = 3):
    """
        Ping list of IP address and return tuple with two lists: reachable and unreachable
    """
    reach_iplist = []
    unreach_iplist = []
    with ThreadPoolExecutor(max_workers=limit) as executor:
        result = executor.map(ping_ip, ip_list)
        for device, output in zip(ip_list, result):
            if output:
                reach_iplist.append(device)
            else:
                unreach_iplist.append(device)
    return (reach_iplist, unreach_iplist)

with open('devices.yaml') as f:
    devices = yaml.safe_load(f)
ip_list_n = []
for device in devices:
    ip_list_n.append(device["ip"])

print(ping_ip_addresses(ip_list_n))


