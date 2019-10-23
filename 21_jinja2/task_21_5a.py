# -*- coding: utf-8 -*-
"""
Задание 21.5a

Создать функцию configure_vpn, которая использует шаблоны из задания 21.5 для настройки VPN на маршрутизаторах на основе данных в словаре data.

Параметры функции:
* src_device_params - словарь с параметрами подключения к устройству
* dst_device_params - словарь с параметрами подключения к устройству
* src_template - имя файла с шаблоном, который создает конфигурацию для одной строны туннеля
* dst_template - имя файла с шаблоном, который создает конфигурацию для второй строны туннеля
* vpn_data_dict - словарь со значениями, которые надо подставить в шаблоны

Функция должна настроить VPN на основе шаблонов и данных на каждом устройстве.
Функция возвращает вывод с набором команд с двух марушртизаторов (вывод, которые возвращает send_config_set).

При этом, в словаре data не указан номер интерфейса Tunnel, который надо использовать.
Номер надо определить самостоятельно на основе информации с оборудования.
Если на маршрутизаторе нет интерфейсов Tunnel, взять номер 0, если есть взять ближайший свободный номер,
но одинаковый для двух маршрутизаторов.

Например, если на маршрутизаторе src такие интерфейсы: Tunnel1, Tunnel4.
А на маршрутизаторе dest такие: Tunnel2, Tunnel3, Tunnel8.
Первый свободный номер одинаковый для двух маршрутизаторов будет 9.
И надо будет настроить интерфейс Tunnel 9.

Для этого задания нет теста!
"""

from task_21_5 import create_vpn_config
from netmiko import ConnectHandler
import yaml
from pprint import pprint


data = {
    'tun_num': None,
    'wan_ip_1': '192.168.100.1',
    'wan_ip_2': '192.168.100.2',
    'tun_ip_1': '10.0.1.1 255.255.255.252',
    'tun_ip_2': '10.0.1.2 255.255.255.252'
}
tunnels1 = 'interface Tunnel1\ninterface Tunnel11\ninterface Tunnel12\n'
tunnels2 = 'interface Tunnel1\ninterface Tunnel13\ninterface Tunnel14\n'
def tunnel_num(dev, tunnels = None):
    if tunnels:
        if "Tunnel" in tunnels:
            tun_list = sorted(tunnels.split('\n'))
            num = int(tun_list[-1].lstrip("interface Tunnel"))
        else:
            num = 0
    else:
        with ConnectHandler(**dev) as ssh:
            ssh.enable()
            tunnels = ssh.send_command("show run | i Tunnel")
            if "Tunnel" in tunnels:
                tun_list = tunnels.split('\n').sort()
                num = int(tun_list[-1].lstrip("interface Tunnel"))
            else:
                num = 0
    return num
def send_show_command(dev, com):
    result_dict = {}
    with ConnectHandler(**dev) as ssh:
        ssh.enable()
        result = ssh.send_config_set(com)
        key = dev['ip']
        result_dict[key] = result
        return result_dict

def configure_vpn(src_device_params, dst_device_params, src_template, dst_template, vpn_data_dict):
    with open(src_device_params) as f:
        src_device = yaml.safe_load(f)
    with open(dst_device_params) as f:
        dst_device = yaml.safe_load(f)
    src_num = tunnel_num(src_device, tunnels = tunnels1)
    dst_num = tunnel_num(dst_device, tunnels = tunnels2)
    if src_num  >= dst_num :
        t_num = src_num + 1
    else:
        t_num = dst_num + 1
    vpn_data_dict['tun_num'] = t_num
    conf1, conf2 = create_vpn_config(src_template, dst_template, vpn_data_dict)
    with open('task_21_6_result1.txt', 'w') as f:
        f.write(conf1)
    with open('task_21_6_result2.txt', 'w') as f:
        f.write(conf2)
    commands1 = conf1.split('\n')
    commands2 = conf2.split('\n')
    print("The number of tunnel is {}".format(t_num))
    pprint(commands1)
    pprint(commands2)
    pprint(send_show_command(src_device, commands1))
    pprint(send_show_command(dst_device, commands2))


configure_vpn('C:/Users/snowowl/PycharmProjects/Natenka_python_tasks/21_jinja2/data_files/src.yaml',
              'C:/Users/snowowl/PycharmProjects/Natenka_python_tasks/21_jinja2/data_files/dst.yaml',
              'gre_ipsec_vpn_1.txt',
              'gre_ipsec_vpn_2.txt',
              data)
