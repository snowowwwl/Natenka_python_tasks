# -*- coding: utf-8 -*-

'''
Задание 27.2d

Дополнить класс MyNetmiko из задания 27.2c или задания 27.2b.

Добавить параметр ignore_errors в метод send_config_set.
Если передано истинное значение, не надо выполнять проверку на ошибки и метод должен работать точно так же как метод send_config_set в netmiko.

Если значение ложное, ошибки должны проверяться.

По умолчанию ошибки должны игнорироваться.


In [2]: from task_27_2d import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [6]: r1.send_config_set('lo')
Out[6]: 'config term\nEnter configuration commands, one per line.  End with CNTL/Z.\nR1(config)#lo\n% Incomplete command.\n\nR1(config)#end\nR1#'

In [7]: r1.send_config_set('lo', ignore_errors=True)
Out[7]: 'config term\nEnter configuration commands, one per line.  End with CNTL/Z.\nR1(config)#lo\n% Incomplete command.\n\nR1(config)#end\nR1#'

In [8]: r1.send_config_set('lo', ignore_errors=False)
---------------------------------------------------------------------------
ErrorInCommand                            Traceback (most recent call last)
<ipython-input-8-704f2e8d1886> in <module>()
----> 1 r1.send_config_set('lo', ignore_errors=False)

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
    def send_command(self,command_string, **kwargs):
        result = super().send_command(command_string)
        return self._check_error_in_command(command_string, result)

    def send_config_set(self, command_list, ignore_errors = True):
        output = ""
        if ignore_errors:
            output = super().send_config_set(command_list)
        else:
            for command in command_list:
                output += self.send_command(command)
        return output



r1 = MikrotikNetmiko(**device_params)
print(r1.send_config_set(['interface 5','interface print'],ignore_errors = False ))