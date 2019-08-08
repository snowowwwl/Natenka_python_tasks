# -*- coding: utf-8 -*-
"""
Задание 18.1

create_db.py
* сюда должна быть вынесена функциональность по созданию БД:
 * должна выполняться проверка наличия файла БД
 * если файла нет, согласно описанию схемы БД в файле dhcp_snooping_schema.sql,
   должна быть создана БД (БД отличается от примера в разделе)

В БД теперь две таблицы (схема описана в файле dhcp_snooping_schema.sql):
 * switches - в ней находятся данные о коммутаторах
 * dhcp - эта таблица осталась такой же как в примере, за исключением поля switch
  * это поле ссылается на поле hostname в таблице switches

Код должен быть разбит на функции.
Какие именно функции и как разделить код, надо решить самостоятельно.
Часть кода может быть глобальной
"""



import os
import sqlite3

db_filename = 'dhcp_snooping.db'
schema_filename = 'dhcp_snooping_schema.sql'

def create_db(db_f, schema_f):
    db_exists = os.path.exists(db_f)
    conn = sqlite3.connect(db_f)
    if not db_exists:
        print('Creating schema...')
        with open(schema_f, 'r') as f:
            schema = f.read()
        conn.executescript(schema)
        print('Done')
    else:
        print('Database exists, assume dhcp and swithes table does, too.')

if __name__ == "__main__":
    create_db(db_filename, schema_filename)
