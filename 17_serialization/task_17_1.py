# -*- coding: utf-8 -*-
"""
Задание 17.1

В этом задании нужно:
* взять содержимое нескольких файлов с выводом команды sh version
* распарсить вывод команды с помощью регулярных выражений и получить информацию об устройстве
* записать полученную информацию в файл в CSV формате

Для выполнения задания нужно создать две функции.

Функция parse_sh_version:
* ожидает аргумент output в котором находится вывод команды sh version (не имя файла)
* обрабатывает вывод, с помощью регулярных выражений
* возвращает кортеж из трёх элементов:
 * ios - в формате "12.4(5)T"
 * image - в формате "flash:c2800-advipservicesk9-mz.124-5.T.bin"
 * uptime - в формате "5 days, 3 hours, 3 minutes"

Функция write_to_csv:
* ожидает два аргумента:
 * имя файла, в который будет записана информация в формате CSV
 * данные в виде списка списков, где:
    * первый список - заголовки столбцов,
    * остальные списки - содержимое
* функция записывает содержимое в файл, в формате CSV и ничего не возвращает

Остальное содержимое скрипта может быть в скрипте, а может быть в ещё одной функции.

Скрипт должен:
* обработать информацию из каждого файла с выводом sh version:
 * sh_version_r1.txt, sh_version_r2.txt, sh_version_r3.txt
* с помощью функции parse_sh_version, из каждого вывода должна быть получена информация ios, image, uptime
* из имени файла нужно получить имя хоста
* после этого вся информация должна быть записана в файл routers_inventory.csv

В файле routers_inventory.csv должны быть такие столбцы:
* hostname, ios, image, uptime

В скрипте, с помощью модуля glob, создан список файлов, имя которых начинается на sh_vers.
Вы можете раскомментировать строку print(sh_version_files), чтобы посмотреть содержимое списка.

Кроме того, создан список заголовков (headers), который должен быть записан в CSV.
"""

import glob
import re
import csv


sh_version_files = glob.glob('sh_vers*')
headers = ['hostname', 'ios', 'image', 'uptime']
hostname_list = list()
hostname_list.append(headers)


def parse_sh_version(sh_ver_output):
    output = sh_ver_output.split('\n')
    for lines in output:
        match = re.search('Version (?P<ios>.+),|'
                          'System image file is "(?P<image>.+)"|'
                          'router uptime is (?P<uptime>.+)', lines)
        if match:
            if match.lastgroup == 'ios':
                ios: str = match.group(match.lastgroup)
            if match.lastgroup == 'image':
                image: str = match.group(match.lastgroup)
            if match.lastgroup == 'uptime':
                uptime: str = match.group(match.lastgroup)
    return ios, image, uptime


def write_to_csv(filename, list_of_hosts):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        for row in list_of_hosts:
            writer.writerow(row)


for file_name in sh_version_files:
    host_list = []
    host = re.search('version_(.+).txt', file_name)
    with open(file_name) as fn:
        ios_image_uptime = list(parse_sh_version(fn.read()))
        host_list.append(host.group(1))
        host_list = host_list+ios_image_uptime
    hostname_list.append(host_list)
write_to_csv('routers_inventory.csv', hostname_list)

with open('routers_inventory.csv') as f:
    print(f.read())
