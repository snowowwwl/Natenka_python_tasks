# -*- coding: utf-8 -*-

'''
Задание 27.1a

Дополнить класс CiscoSSH из задания 27.1.

Перед подключением по SSH необходимо проверить если ли в словаре
с параметрами подключения такие параметры: username, password, secret.
Если нет, запросить их у пользователя, а затем выполнять подключение.

In [1]: from task_27_1a import CiscoSSH

In [2]: device_params = {
   ...:         'device_type': 'cisco_ios',
   ...:         'ip': '192.168.100.1',
   ...: }

In [3]: r1 = CiscoSSH(**device_params)
Введите имя пользователя: cisco
Введите пароль:
Введите пароль для режима enable:

In [4]: r1.send_show_command('sh ip int br')
Out[4]: 'Interface                  IP-Address      OK? Method Status                Protocol\nEthernet0/0                192.168.100.1   YES NVRAM  up                    up      \nEthernet0/1                192.168.200.1   YES NVRAM  up                    up      \nEthernet0/2                190.16.200.1    YES NVRAM  up                    up      \nEthernet0/3                192.168.230.1   YES NVRAM  up                    up      \nEthernet0/3.100            10.100.0.1      YES NVRAM  up                    up      \nEthernet0/3.200            10.200.0.1      YES NVRAM  up                    up      \nEthernet0/3.300            10.30.0.1       YES NVRAM  up                    up      '

'''

device_params = {
    'device_type': 'mikrotik_routeros',
    'ip': '192.168.88.1'
}

from base_connect_class import BaseSSH

class MikrotikSSH(BaseSSH):
    def __init__(self,**device_params):
        if not device_params.get("username"):
            username = input("Enter username: ")
            device_params['username'] = username
        if not device_params.get("password"):
            password = input("Enter password: ")
            device_params['password'] = password
        print(device_params)
        ssh = super().__init__(**device_params)
        self.ssh.send_command('interface print')





r1 = MikrotikSSH(**device_params)
print(r1.send_show_command('interface print'))