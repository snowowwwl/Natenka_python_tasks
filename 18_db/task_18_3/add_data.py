# -*- coding: utf-8 -*-
"""
Задание 18.3

В прошлых заданиях информация добавлялась в пустую БД.
В этом задании, разбирается ситуация, когда в БД уже есть информация.

Скопируйте скрипт add_data.py и попробуйте выполнить его повторно, на существующей БД.
Должна возникнуть ошибка.

При создании схемы БД, было явно указано, что поле MAC-адрес, должно быть уникальным.
Поэтому, при добавлении записи с таким же MAC-адресом, возникает ошибка.

Но, нужно каким-то образом обновлять БД, чтобы в ней хранилась актуальная информация.

Например, можно каждый раз, когда записывается информация,
предварительно просто удалять всё из таблицы dhcp.

Но, в принципе, старая информация тоже может пригодиться.

Поэтому, мы будем делать немного по-другому.
Создадим новое поле active, которое будет указывать является ли запись актуальной.

Поле active должно принимать такие значения:
* 0 - означает False. И используется для того, чтобы отметить запись как неактивную
* 1 - True. Используется чтобы указать, что запись активна

Каждый раз, когда информация из файлов с выводом DHCP snooping добавляется заново,
надо пометить все существующие записи (для данного коммутатора), как неактивные (active = 0).
Затем можно обновлять информацию и пометить новые записи, как активные (active = 1).


Таким образом, в БД останутся и старые записи, для MAC-адресов, которые сейчас не активны,
и появится обновленная информация для активных адресов.

Новая схема БД находится в файле dhcp_snooping_schema.sql

Измените скрипт add_data.py таким образом, чтобы выполнялись новые условия и заполнялось поле active.

Код в скрипте должен быть разбит на функции.
Какие именно функции и как разделить код, надо решить самостоятельно.
Часть кода может быть глобальной.

> Для проверки корректности запроса SQL, можно выполнить его в командной строке, с помощью утилиты sqlite3.

Для проверки задания и работы нового поля, попробуйте удалить пару строк
из одного из файлов с выводом dhcp snooping.
И после этого проверить, что удаленные строки отображаются в таблице как неактивные.
"""

import glob
import re
import yaml
import sqlite3
import os
from get_data import get_data

db_filename = 'dhcp_snooping.db'
dhcp_snoop_files = glob.glob('sw*_dhcp_snooping.txt')


def add_switches(ymlfile, files_list):
    hostname_list = []
    sw_tuple_list = []
    for dhcpfile in files_list:
        hostname = re.match('(.+?)_', dhcpfile)
        if hostname:
            hostname_list.append(hostname.group(1))

    db_exists = os.path.exists(db_filename)
    if not db_exists:
        print("Please create DB first with help of function create_db(db_f, schema_f)")
    else:
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
    active = 1
    for dhcpfile in files_list:
        with open(dhcpfile) as data:
            for line in data:
                match = regex.search(line)
                if match:
                    result.append((match.group(1), match.group(2), match.group(3), match.group(4), hostname_list[i], active))
        i+=1
    print(result)

    db_exists = os.path.exists(db_filename)

    if not db_exists:
        print("Please create DB first with help of function create_db(db_f, schema_f)")
    else:
        print('Inserting DHCP Snooping data')
        conn = sqlite3.connect(db_filename)
        for host in hostname_list:
            conn.execute("update dhcp set active = 0 where switch = ?", [host])
            conn.commit()
        for row in result:
            try:
                with conn:
                    query = '''replace into dhcp (mac, ip, vlan, interface, switch, active)
                                values (?, ?, ?, ?, ?, ?)'''
                    conn.execute(query, row)
            except sqlite3.IntegrityError as e:
                print('Error occured: ', e)

        print('Inserting DHCP Snooping data done')
        conn.commit()
        conn.close()
