# -*- coding: utf-8 -*-

'''
Задание 26.2

Добавить к классу CiscoTelnet из задания 25.2x поддержку работы в менеджере контекста.
При выходе из блока менеджера контекста должно закрываться соединение.
Все исключения, которые возникли в менеджере контекста, должны генерироваться после выхода из блока with.

Пример работы:

In [14]: r1_params = {
    ...:     'ip': '192.168.100.1',
    ...:     'username': 'cisco',
    ...:     'password': 'cisco',
    ...:     'secret': 'cisco'}

In [15]: from task_26_2 import CiscoTelnet

In [16]: with CiscoTelnet(**r1_params) as r1:
    ...:     print(r1.send_show_command('sh clock'))
    ...:
sh clock
*19:17:20.244 UTC Sat Apr 6 2019
R1#

In [17]: with CiscoTelnet(**r1_params) as r1:
    ...:     print(r1.send_show_command('sh clock'))
    ...:     raise ValueError('Возникла ошибка')
    ...:
sh clock
*19:17:38.828 UTC Sat Apr 6 2019
R1#
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-17-f3141be7c129> in <module>
      1 with CiscoTelnet(**r1_params) as r1:
      2     print(r1.send_show_command('sh clock'))
----> 3     raise ValueError('Возникла ошибка')
      4

ValueError: Возникла ошибка
'''

import telnetlib
import time
from pprint import pprint
import textfsm

r1_params = {
    'ip': '192.168.88.1',
    'username': 'admin',
    'password': 'disoriac'
    }

class CiscoTelnet():
    def __init__(self, params):
        tn = telnetlib.Telnet(params['ip'])
        tn.read_until(b"Login: ")
        username = self._write_line(params['username'])
        tn.write(username)
        tn.read_until(b"Password: ")
        tn.write(self._write_line(params['password']))
        self.tn = tn
    def _write_line(self,line):
       return bytes(line+"\r\n",'utf-8')
    def send_show_command(self,command, template_file, parse = False):
        self.tn.read_until(b'[admin@MikroTik] > ')
        self.tn.write(self._write_line(command))
        pprint(self._write_line(command))
        time.sleep(2)
        output = self.tn.read_very_eager().decode('ascii')
        if parse == False:
            return output
        else:
            with open(template_file) as template:
                fsm = textfsm.TextFSM(template)
                result = fsm.ParseText(output)
            result_list = []
            result_list.append((fsm.header))
            result_list.append(result)
            return result_list
    def send_config_commands(self,command_list):
        if type(command_list) == str:
            self.tn.read_until(b'[admin@MikroTik] > ')
            self.tn.write(self._write_line(command_list))
            pprint(self._write_line(command_list))
            time.sleep(2)
            output = self.tn.read_very_eager().decode('ascii')
        if type(command_list) == list:
            for command in command_list:
                self.tn.read_until(b'[admin@MikroTik] > ')
                self.tn.write(self._write_line(command))
                pprint(self._write_line(command))
                time.sleep(2)
            output = self.tn.read_very_eager().decode('ascii')
        return output

    def __enter__(self):
        print('__ENTER__')
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print('__EXIT__')
        self.tn.close()


with CiscoTelnet(r1_params) as r1:
    print(r1.send_show_command('interface print',
                     'C:/Users/snowowl/PycharmProjects/Natenka_python_tasks/25_oop_basics/templates/interface_print_mik',
                     parse = True))
