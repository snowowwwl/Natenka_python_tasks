# -*- coding: utf-8 -*-
"""
Задание 7.2c

Переделать скрипт из задания 7.2b:
* передавать как аргументы скрипту:
 * имя исходного файла конфигурации
 * имя итогового файла конфигурации

Внутри, скрипт должен отфильтровать те строки, в исходном файле конфигурации,
в которых содержатся слова из списка ignore.
И записать остальные строки в итоговый файл.

Проверить работу скрипта на примере файла config_sw1.txt.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""

ignore = ['duplex', 'alias', 'Current configuration']

from sys import argv

filename_src, filename_dst = argv[1:]
with open(filename_src, 'r') as src, open(filename_dst, 'w') as dest:
    for line in src:
        for word in ignore:
            if line.count(word) >= 1:
                break
        else:
            dest.write(line)