# -*- coding: utf-8 -*-
'''
Задание 18.5a

После выполнения задания 18.5, в таблице dhcp есть новое поле last_active.

Обновите скрипт add_data.py, таким образом, чтобы он удалял все записи,
которые были активными более 7 дней назад.

Для того, чтобы получить такие записи, можно просто вручную обновить поле last_active.

В файле задания описан пример работы с объектами модуля datetime.
Обратите внимание, что объекты, как и строки с датой, которые пишутся в БД,
можно сравнивать между собой.

'''
import datetime as dt
from datetime import timedelta, datetime
import glob
from create_db import create_db
from add_data import add_data
from get_data import get_data
import sqlite3

now = datetime.today().replace(microsecond=0)
week_ago = now - timedelta(days=7)

db_filename = 'dhcp_snooping.db'
schema_filename = 'dhcp_snooping_schema.sql'
dhcp_snoop_files = glob.glob('sw*_dhcp_snooping.txt')

hostnames = ['sw1', 'sw2', 'sw3']
create_db(db_filename, schema_filename)
add_data(dhcp_snoop_files, hostnames)
get_data()
conn = sqlite3.connect(db_filename)
conn.execute("update dhcp set last_active = '2019-08-01 15:08:22' where switch = 'sw1'")
conn.commit()
conn.close()
get_data()
add_data(dhcp_snoop_files, hostnames)
get_data()
