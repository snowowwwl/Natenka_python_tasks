# -*- coding: utf-8 -*-

'''
Задание 27.2b

Дополнить класс MyNetmiko из задания 27.2a.

Переписать метод send_config_set netmiko, добавив в него проверку на ошибки с помощью метода _check_error_in_command.

Метод send_config_set должен отправлять команды по одной и проверять каждую на ошибки.
Если при выполнении команд не обнаружены ошибки, метод send_config_set возвращает вывод команд.

In [2]: from task_27_2b import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [4]: r1.send_config_set('lo')
---------------------------------------------------------------------------
ErrorInCommand                            Traceback (most recent call last)
<ipython-input-2-8e491f78b235> in <module>()
----> 1 r1.send_config_set('lo')

...
ErrorInCommand: При выполнении команды "lo" на устройстве 192.168.100.1 возникла ошибка "Incomplete command."

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
    def send_command(self,command_string):
        result = super().send_command(command_string)
        return self._check_error_in_command(command_string, result)

    def send_config_set(self, command_list):
        output=""
        for command in command_list:
            output += self.send_command(command)
        return output



r1 = MikrotikNetmiko(**device_params)
print(r1.send_config_set(['ping 8.8.8.8 c 3','interface print']))