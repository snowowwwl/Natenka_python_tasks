# -*- coding: utf-8 -*-
"""
Задание 11.1

Создать функцию parse_cdp_neighbors, которая обрабатывает
вывод команды show cdp neighbors.

Функция ожидает, как аргумент, вывод команды одной строкой.

Функция должна возвращать словарь, который описывает соединения между устройствами.

Например, если как аргумент был передан такой вывод:
R4>show cdp neighbors

Device ID    Local Intrfce   Holdtme     Capability       Platform    Port ID
R5           Fa 0/1          122           R S I           2811       Fa 0/1
R6           Fa 0/2          143           R S I           2811       Fa 0/0

Функция должна вернуть такой словарь:

    {('R4', 'Fa0/1'): ('R5', 'Fa0/1'),
     ('R4', 'Fa0/2'): ('R6', 'Fa0/0')}

Интерфейсы могут быть записаны с пробелом Fa 0/0 или без Fa0/0.

Проверить работу функции на содержимом файла sw1_sh_cdp_neighbors.txt

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""


def parse_cdp_neighbors(cdpstring):
    """

    :param cdpstring: the output of command "show cdp neighbors" in string
    :return: Dictionary of neighbors and ports , looks like
    {('R4', 'Fa0/1'): ('R5', 'Fa0/1'),
     ('R4', 'Fa0/2'): ('R6', 'Fa0/0')}
    """
    cdp_ne_dict = {}
    local_ports = []
    local_devices = []
    remote_ports = []
    remote_devices = []
    flag = 0
    cdp_list = cdpstring.split('\n')
    cdp_list.pop(-1)
    local_device = str()
    for line in cdp_list:
        if line.startswith('\n'):
            pass
        elif line.startswith("Device ID"):
            flag = 1
        elif '>' in line:
            local_device = line.split('>')[0]
            print(local_device)
        else:
            if flag == 1:
                device_list = line.split()
                if len(device_list)>0:
                    remote_device = device_list[0]
                    local_port = device_list[1]+device_list[2]
                    remote_port = device_list[-2]+device_list[-1]
                    local_ports.append(local_port)
                    remote_ports.append(remote_port)
                    local_devices.append(local_device)
                    remote_devices.append(remote_device)
                    cdpkey = list(zip(local_devices, local_ports))
                    cdpvalue = list(zip(remote_devices, remote_ports))
                    cdp_ne_dict = dict(zip(cdpkey, cdpvalue))
                else:
                    pass
    return cdp_ne_dict


with open('C:/Users/snowowl/PycharmProjects/Natenka_python_tasks/11_modules/sw1_sh_cdp_neighbors.txt', 'r') as f:
    showcdpne = f.read()
if __name__ == "__main__":
    print(parse_cdp_neighbors(showcdpne))
