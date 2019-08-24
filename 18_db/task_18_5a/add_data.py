# -*- coding: utf-8 -*-
"""
Задание 18.5

"""

import datetime as dt
from datetime import timedelta, datetime
import glob
import re
import yaml
import sqlite3
import os


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
    now = datetime.today().replace(microsecond=0)
    week_ago = now - timedelta(days=7)
    for dhcpfile in files_list:
        with open(dhcpfile) as data:
            for line in data:
                match = regex.search(line)
                if match:
                    last_active = str(dt.datetime.today().replace(microsecond=0))
                    result.append((match.group(1), match.group(2), match.group(3), match.group(4), hostname_list[i], active, last_active))
        i+=1

    db_exists = os.path.exists(db_filename)
    if not db_exists:
        print("Please create DB first with help of function create_db(db_f, schema_f)")
    else:
        print('Delete rows older then 7 days:')
        conn = sqlite3.connect(db_filename)
        conn.execute('delete from dhcp where last_active < ?', [str(week_ago)])
        print('Inserting DHCP Snooping data')
        for host in hostname_list:
            conn.execute("update dhcp set active = 0 where switch = ?", [host])
            conn.commit()
        for row in result:
            try:
                with conn:
                    query = '''replace into dhcp (mac, ip, vlan, interface, switch, active, last_active)
                                values (?, ?, ?, ?, ?, ?, ?)'''
                    conn.execute(query, row)
            except sqlite3.IntegrityError as e:
                print('Error occured: ', e)

        print('Inserting DHCP Snooping data done')
        conn.commit()
        conn.close()
