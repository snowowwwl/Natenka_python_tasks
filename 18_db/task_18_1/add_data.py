# -*- coding: utf-8 -*-
"""
Задание 18.1

add_data.py
* с помощью этого скрипта, выполняется добавление данных в БД
* добавлять надо не только данные из вывода sh ip dhcp snooping binding, но и информацию о коммутаторах


В файле add_data.py должны быть две части:
* информация о коммутаторах добавляется в таблицу switches
 * данные о коммутаторах, находятся в файле switches.yml
* информация на основании вывода sh ip dhcp snooping binding добавляется в таблицу dhcp
 * вывод с трёх коммутаторов:
   * файлы sw1_dhcp_snooping.txt, sw2_dhcp_snooping.txt, sw3_dhcp_snooping.txt
 * так как таблица dhcp изменилась, и в ней теперь присутствует поле switch, его нужно также заполнять. Имя коммутатора определяется по имени файла с данными

Код должен быть разбит на функции.
Какие именно функции и как разделить код, надо решить самостоятельно.
Часть кода может быть глобальной.
"""

import glob
import re
import yaml
import sqlite3


db_filename = 'dhcp_snooping.db'
dhcp_snoop_files = glob.glob('sw*_dhcp_snooping.txt')
#print(dhcp_snoop_files)


def add_switches(ymlfile, files_list):
    hostname_list = []
    sw_tuple_list = []
    for dhcpfile in files_list:
        hostname = re.match('(.+?)_', dhcpfile)
        if hostname:
            hostname_list.append(hostname.group(1))
    conn = sqlite3.connect(db_filename)
    print('Inserting hostnames')
    with open('switches.yml') as f:
        switches = yaml.load(f.read(), Loader=yaml.FullLoader)
    for host in hostname_list:
        sw_tuple_list.append((host, switches['switches'][host]))
    for sw in sw_tuple_list:
        try:
            with conn:
                query = '''insert into switches (hostname, location)
                               values (?, ?)'''
                conn.execute(query, sw)
        except sqlite3.IntegrityError as e:
            print('Error occured: ', e)
    print('Inserting hostnames done')
    conn.commit()
    conn.close()
    return hostname_list


def add_data(files_list, hostname_list):
    regex = re.compile('(\S+) +(\S+) +\d+ +\S+ +(\d+) +(\S+)')
    result = []
    i = 0
    for dhcpfile in files_list:
        with open(dhcpfile) as data:
            for line in data:
                match = regex.search(line)
                if match:
                    result.append((match.group(1), match.group(2), match.group(3), match.group(4), hostname_list[i]))
        i+=1
    print('Inserting DHCP Snooping data')
    conn = sqlite3.connect(db_filename)
    for row in result:
        try:
            with conn:
                query = '''insert into dhcp (mac, ip, vlan, interface, switch)
                            values (?, ?, ?, ?, ?)'''
                conn.execute(query, row)
        except sqlite3.IntegrityError as e:
            print('Error occured: ', e)
    print('Inserting DHCP Snooping data done')
    conn.commit()
    conn.close()
