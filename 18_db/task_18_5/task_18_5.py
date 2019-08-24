# -*- coding: utf-8 -*-
'''
Задание 18.5

Теперь в БД остается и старая информация.
И, если какой-то MAC-адрес не появлялся в новых записях, запись с ним,
может оставаться в БД очень долго.

И, хотя это может быть полезно, чтобы посмотреть, где MAC-адрес находился в последний раз,
постоянно хранить эту информацию не очень полезно.

Например, если запись в БД уже больше месяца, то её можно удалить.

Для того, чтобы сделать такой критерий, нужно ввести новое поле,
в которое будет записываться последнее время добавления записи.

Новое поле называется last_active и в нем должна находиться строка,
в формате: YYYY-MM-DD HH:MM:SS.

В этом задании необходимо:
* изменить, соответственно, таблицу dhcp и добавить новое поле.
 * таблицу можно поменять из cli sqlite, но файл dhcp_snooping_schema.sql тоже необходимо изменить
* изменить скрипт add_data.py, чтобы он добавлял к каждой записи время

Как получить строку со временем и датой, в указанном формате, показано в задании.
Раскомментируйте строку и посмотрите как она выглядит.

'''

import datetime
import glob
from create_db import create_db
from add_data import add_data
from get_data import get_data

now = str(datetime.datetime.today().replace(microsecond=0))
print(now)

db_filename = 'dhcp_snooping.db'
schema_filename = 'dhcp_snooping_schema.sql'
dhcp_snoop_files = glob.glob('sw*_dhcp_snooping.txt')

hostnames = ['sw1', 'sw2', 'sw3']
create_db(db_filename, schema_filename)
add_data(dhcp_snoop_files, hostnames)

get_data()