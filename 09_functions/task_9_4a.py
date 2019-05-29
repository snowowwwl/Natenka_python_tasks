# -*- coding: utf-8 -*-
'''
Задание 9.4a

Задача такая же, как и задании 9.4.
Проверить работу функции надо на примере файла config_r1.txt

Обратите внимание на конфигурационный файл.
В нем есть разделы с большей вложенностью, например, разделы:
* interface Ethernet0/3.100
* router bgp 100

Надо чтобы функция config_to_dict обрабатывала следующий уровень вложенности.
При этом, не привязываясь к конкретным разделам.
Она должна быть универсальной, и сработать, если это будут другие разделы.

Если уровня вложенности два:
* то команды верхнего уровня будут ключами словаря,
* а команды подуровней - списками

Если уровня вложенности три:
* самый вложенный уровень должен быть списком,
* а остальные - словарями.

На примере interface Ethernet0/3.100:

{'interface Ethernet0/3.100':{
               'encapsulation dot1Q 100':[],
               'xconnect 10.2.2.2 12100 encapsulation mpls':
                   ['backup peer 10.4.4.4 14100',
                    'backup delay 1 1']}}


Ограничение: Все задания надо выполнять используя только пройденные темы.

'''

ignore = ['duplex', 'alias', 'Current configuration']

from pprint import pprint

def check_ignore(command, ignore):
    '''
    Функция проверяет содержится ли в команде слово из списка ignore.

    command - строка. Команда, которую надо проверить
    ignore - список. Список слов

    Возвращает True, если в команде содержится слово из списка ignore, False - если нет

    '''
    return any(word in command for word in ignore)

def level(string):
    if string[0] == ' ' and string[1] == ' ':
        level = 2
    elif string[0] == ' ' and not string[1] == ' ':
        level = 1
    else: level =0
    return level

def config_as_dict(configfile):
    port_dict1 = {}
    port_dict2 = {}
    with open(configfile, 'r') as f:
        config_list = f.readlines()
        for i in range(len(config_list)):
            commands1 = []
            commands2 = []
            line = config_list[i]
            if check_ignore(line,ignore):
                pass
            elif line.startswith('!'):
                pass
            elif level(line) == 0:
                key1 = line.strip('\n')
                flag = 0
                for l in config_list[i+1::]:
                    if level(l) == 1:
                        commands1.append(l.strip('\n'))
                        key2 = l.strip('\n')
                    elif level(l) == 2:
                        flag = 2
                        commands2.append(l.strip('\n'))
                    else:
                        break
                if flag == 2:
                    port_dict2 = {key: [] for key in commands1}
                    port_dict2[key2] = commands2
                    port_dict1[key1] = port_dict2
                else:
                    port_dict1[key1] = commands1


    return port_dict1


pprint(config_as_dict('C:/Users/snowowl/PycharmProjects/Natenka_python_tasks/09_functions/config_r1.txt'))