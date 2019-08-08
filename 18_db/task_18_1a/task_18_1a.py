# -*- coding: utf-8 -*-
"""
Задание 18.1a

Скопировать скрипт add_data.py из задания 18.1.

Добавить в файл add_data.py проверку на наличие БД:
* если файл БД есть, записать данные
* если файла БД нет, вывести сообщение, что БД нет и её необходимо сначала создать

"""

import sys
import glob
from create_db import create_db
from add_data import add_data
from add_data import add_switches
sys.path.insert(0, 'C:/Users/snowowl/PycharmProjects/Natenka_python_tasks/18_db/')

db_filename = 'dhcp_snooping.db'
schema_filename = 'dhcp_snooping_schema.sql'
dhcp_snoop_files = glob.glob('sw*_dhcp_snooping.txt')


create_db(db_filename, schema_filename)
add_data(dhcp_snoop_files, add_switches('switches.yml', dhcp_snoop_files))

