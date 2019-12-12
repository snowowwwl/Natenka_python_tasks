# -*- coding: utf-8 -*-

'''
Задание 27.2c

Проверить, что метод send_command класса MyNetmiko из задания 27.2b, принимает дополнительные аргументы (как в netmiko), кроме команды.

Если возникает ошибка, переделать метод таким образом, чтобы он принимал любые аргументы, которые поддерживает netmiko.


In [2]: from task_27_2c import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [4]: r1.send_command('sh ip int br', strip_command=False)
Out[4]: 'sh ip int br\nInterface                  IP-Address      OK? Method Status                Protocol\nEthernet0/0                192.168.100.1   YES NVRAM  up                    up      \nEthernet0/1                192.168.200.1   YES NVRAM  up                    up      \nEthernet0/2                190.16.200.1    YES NVRAM  up                    up      \nEthernet0/3                192.168.230.1   YES NVRAM  up                    up      \nEthernet0/3.100            10.100.0.1      YES NVRAM  up                    up      \nEthernet0/3.200            10.200.0.1      YES NVRAM  up                    up      \nEthernet0/3.300            10.30.0.1       YES NVRAM  up                    up      '

In [5]: r1.send_command('sh ip int br', strip_command=True)
Out[5]: 'Interface                  IP-Address      OK? Method Status                Protocol\nEthernet0/0                192.168.100.1   YES NVRAM  up                    up      \nEthernet0/1                192.168.200.1   YES NVRAM  up                    up      \nEthernet0/2                190.16.200.1    YES NVRAM  up                    up      \nEthernet0/3                192.168.230.1   YES NVRAM  up                    up      \nEthernet0/3.100            10.100.0.1      YES NVRAM  up                    up      \nEthernet0/3.200            10.200.0.1      YES NVRAM  up                    up      \nEthernet0/3.300            10.30.0.1       YES NVRAM  up                    up      '

'''
from netmiko.mikrotik.mikrotik_ssh import MikrotikBase
device_params = {
    'device_type': 'mikrotik_routeros',
    'ip': '192.168.88.1',
    'username': 'admin',
    'password': 'disoriac'
}
class ErrorInCommand(Exception):
    """При выполнении команды возникла ошибка"""

class MikrotikNetmiko(MikrotikBase):
    def __init__(self,**device_params):
        ssh = super().__init__(**device_params)
        self.ip = device_params['ip']
    def  _check_error_in_command(self, command, result):
        if "bad command" in result:
            raise ErrorInCommand("There are error on device {} during command execution {} -> {} ".format(self.ip, command, result))
        else:
            return result
    def send_command(self,command_string, **kwargs):
        result = super().send_command(command_string)
        return self._check_error_in_command(command_string, result)

    def send_config_set(self, command_list):
        output=""
        for command in command_list:
            output += self.send_command(command)
        return output



r1 = MikrotikNetmiko(**device_params)
print(r1.send_command('interface print', strip_command=True))