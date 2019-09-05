
"""
Задание 19.1

Создать функцию send_show_command.

Функция подключается по SSH (с помощью netmiko) к устройству и выполняет указанную команду.

Параметры функции:
* device - словарь с параметрами подключения к устройству
* command - команда, которую надо выполнить

Функция возвращает словарь с результатами выполнения команды:
* ключ - IP устройства
* значение - результат выполнения команды

Отправить команду command на все устройства из файла devices.yaml (для этого надо считать информацию из файла)
с помощью функции send_show_command.

"""


from netmiko import ConnectHandler
import yaml
from pprint import pprint

with open('devices.yaml') as f:
    devices = yaml.safe_load(f)
pprint(devices)
commands = ['interface',
            'export compact']


def send_show_command(dev, com):
    result_dict = {}
    with ConnectHandler(**dev) as ssh:
        ssh.enable()
        result = ssh.send_config_set(com)
        key = dev['ip']
        result_dict[key] = result
        return result_dict


for device in devices['routers']:
    pprint(send_show_command(device, commands))
