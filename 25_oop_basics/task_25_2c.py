# -*- coding: utf-8 -*-

'''
Задание 25.2c

Скопировать класс CiscoTelnet из задания 25.2b и изменить метод send_config_commands добавив проверку команд на ошибки.

У метода send_config_commands должен быть дополнительный параметр strict:
* strict=True значит, что при обнаружении ошибки, необходимо сгенерировать исключение ValueError
* strict=False значит, что при обнаружении ошибки, надо только вывести на стандартный поток вывода сообщене об ошибке

Метод дожен возвращать вывод аналогичный методу send_config_set у netmiko (пример вывода ниже).
Текст исключения и ошибки в примере ниже.

Пример создания экземпляра класса:
In [1]: from task_25_2c import CiscoTelnet

In [2]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [3]: r1 = CiscoTelnet(**r1_params)

In [4]: commands_with_errors = ['logging 0255.255.1', 'logging', 'i']
In [5]: correct_commands = ['logging buffered 20010', 'ip http server']
In [6]: commands = commands_with_errors+correct_commands

Использование метода send_config_commands:

In [7]: print(r1.send_config_commands(commands, strict=False))
При выполнении команды "logging 0255.255.1" на устройстве 192.168.100.1 возникла ошибка -> Invalid input detected at '^' marker.
При выполнении команды "logging" на устройстве 192.168.100.1 возникла ошибка -> Incomplete command.
При выполнении команды "i" на устройстве 192.168.100.1 возникла ошибка -> Ambiguous command:  "i"
conf t
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#logging 0255.255.1
                   ^
% Invalid input detected at '^' marker.

R1(config)#logging
% Incomplete command.

R1(config)#i
% Ambiguous command:  "i"
R1(config)#logging buffered 20010
R1(config)#ip http server
R1(config)#end
R1#

In [8]: print(r1.send_config_commands(commands, strict=True))
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-8-0abc1ed8602e> in <module>
----> 1 print(r1.send_config_commands(commands, strict=True))

...

ValueError: При выполнении команды "logging 0255.255.1" на устройстве 192.168.100.1 возникла ошибка -> Invalid input detected at '^' marker.

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
        self.ip = params['ip']
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
    def send_config_commands(self,command_list,strict=False):
        if type(command_list) == str:
            self.tn.read_until(b'[admin@MikroTik] > ')
            self.tn.write(self._write_line(command_list))
            pprint(self._write_line(command_list))
            time.sleep(2)
            output = self.tn.read_very_eager().decode('ascii')
            if strict == False:
                if "bad command" in output:
                    pprint("При выполнении команды {} на устройстве {} возникла ошибка ->\n{} ".format(command_list, self.ip, output))
            if strict == True:
                if"bad command" in output:
                    raise ValueError("При выполнении команды {} на устройстве {} возникла ошибка ->{} ".format(command_list, self.ip,
                                                                                                  output))
        if type(command_list) == list:
            for command in command_list:
                self.tn.read_until(b'[admin@MikroTik] > ')
                self.tn.write(self._write_line(command))
                pprint(self._write_line(command))
                time.sleep(2)
            output = self.tn.read_very_eager().decode('ascii')
            if strict == False:
                if "bad command" in output:
                    pprint("При выполнении команды {} на устройстве {} возникла ошибка ->{} ".format(command_list, self.ip, output))
            if strict == True:
                if "bad command" in output:
                    raise ValueError("При выполнении команды {} на устройстве {} возникла ошибка ->bad command \n {}".format(command_list, self.ip, output))
        return output



r1 = CiscoTelnet(r1_params)
r1.send_config_commands(['interface 5','interface print'], strict = True)