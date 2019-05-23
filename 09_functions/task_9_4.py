# -*- coding: utf-8 -*-
"""
Задание 9.4

Создать функцию, которая обрабатывает конфигурационный файл коммутатора
и возвращает словарь:
* Все команды верхнего уровня (глобального режима конфигурации), будут ключами.
* Если у команды верхнего уровня есть подкоманды, они должны быть в значении у соответствующего ключа, в виде списка (пробелы в начале строки можно оставлять).
* Если у команды верхнего уровня нет подкоманд, то значение будет пустым списком

Функция ожидает в качестве аргумента имя конфигурационного файла.

Проверить работу функции на примере файла config_sw1.txt

При обработке конфигурационного файла, надо игнорировать строки, которые начинаются с '!',
а также строки в которых содержатся слова из списка ignore.

Для проверки надо ли игнорировать строку, использовать функцию ignore_command.


Ограничение: Все задания надо выполнять используя только пройденные темы.
"""

ignore = ['duplex', 'alias', 'Current configuration',]


def ignore_command(command, ignore):
    '''
    Функция проверяет содержится ли в команде слово из списка ignore.

    command - строка. Команда, которую надо проверить
    ignore - список. Список слов

    Возвращает
    * True, если в команде содержится слово из списка ignore
    * False - если нет
    '''
    return any(word in command for word in ignore)


def config_as_dict(file):
    port_dict = {}
    with open(file, 'r') as f:
        config_list = f.readlines()
        for i in range(len(config_list)):
            commands = []
            line = config_list[i]
            if ignore_command(line,ignore):
                pass
            elif '!' in line:
                pass
            elif not line.startswith(' '):
                key = line.strip('\n')
                for l in config_list[i+1::]:
                    if l.startswith(' '):
                        commands.append(l.strip('\n'))
                    else:
                        break
                port_dict[key] = commands
    return port_dict


print(config_as_dict('C:/Users/snowowl/PycharmProjects/Natenka_python_tasks/09_functions/config_sw1.txt'))


