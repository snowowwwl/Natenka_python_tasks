# -*- coding: utf-8 -*-

'''
Задание 25.2a

Скопировать класс CiscoTelnet из задания 25.2 и изменить метод send_show_command добавив два параметра:

* parse - контролирует то, будет возвращаться обычный вывод команды или список словарей, полученные после обработки с
 помощью TextFSM. При parse=True должен возвращаться список словарей, а parse=False обычный вывод
* templates - путь к каталогу с шаблонами



Пример создания экземпляра класса:

In [1]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [2]: from task_25_2a import CiscoTelnet

In [3]: r1 = CiscoTelnet(**r1_params)

Использование метода send_show_command:
In [4]: r1.send_show_command('sh ip int br', parse=False)
Out[4]: 'sh ip int br\r\nInterface                  IP-Address      OK? Method Status                Protocol\r\nEthernet0/0                192.168.100.1   YES NVRAM  up                    up      \r\nEthernet0/1                192.168.200.1   YES NVRAM  up                    up      \r\nEthernet0/2                190.16.200.1    YES NVRAM  up                    up      \r\nEthernet0/3                192.168.130.1   YES NVRAM  up                    up      \r\nEthernet0/3.100            10.100.0.1      YES NVRAM  up                    up      \r\nEthernet0/3.200            10.200.0.1      YES NVRAM  up                    up      \r\nEthernet0/3.300            10.30.0.1       YES NVRAM  up                    up      \r\nLoopback0                  10.1.1.1        YES NVRAM  up                    up      \r\nLoopback55                 5.5.5.5         YES manual up                    up      \r\nR1#'

In [5]: r1.send_show_command('sh ip int br', parse=True)
Out[5]:
[{'intf': 'Ethernet0/0',
  'address': '192.168.100.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Ethernet0/1',
  'address': '192.168.200.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Ethernet0/2',
  'address': '190.16.200.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Ethernet0/3',
  'address': '192.168.130.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Ethernet0/3.100',
  'address': '10.100.0.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Ethernet0/3.200',
  'address': '10.200.0.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Ethernet0/3.300',
  'address': '10.30.0.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Loopback0',
  'address': '10.1.1.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Loopback55',
  'address': '5.5.5.5',
  'status': 'up',
  'protocol': 'up'}]
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



r1 = CiscoTelnet(r1_params)
pprint(r1.send_show_command('interface print',
                     'C:/Users/snowowl/PycharmProjects/Natenka_python_tasks/25_oop_basics/templates/interface_print_mik',
                     parse = True))

