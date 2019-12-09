# -*- coding: utf-8 -*-

'''
Задание 25.2b

Скопировать класс CiscoTelnet из задания 25.2a и добавить метод send_config_commands.


Метод send_config_commands должен уметь отправлять одну команду конфигурационного режима или список команд.
Метод должен возвращать вывод аналогичный методу send_config_set у netmiko (пример вывода ниже).

Пример создания экземпляра класса:
In [1]: from task_25_2b import CiscoTelnet

In [2]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [3]: r1 = CiscoTelnet(**r1_params)

Использование метода send_config_commands:

In [5]: r1.send_config_commands('logging 10.1.1.1')
Out[5]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#logging 10.1.1.1\r\nR1(config)#end\r\nR1#'

In [6]: r1.send_config_commands(['interface loop55', 'ip address 5.5.5.5 255.255.255.255'])
Out[6]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#interface loop55\r\nR1(config-if)#ip address 5.5.5.5 255.255.255.255\r\nR1(config-if)#end\r\nR1#'

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



r1 = CiscoTelnet(r1_params)
pprint(r1.send_config_commands(['interface print','ping 8.8.8.8']))


