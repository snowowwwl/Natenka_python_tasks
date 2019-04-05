# -*- coding: utf-8 -*-
"""
Задание 5.3a

Дополнить скрипт из задания 5.3 таким образом, чтобы, в зависимости от выбранного режима,
задавались разные вопросы в запросе о номере VLANа или списка VLANов:
* для access: 'Enter VLAN number:'
* для trunk: 'Enter allowed VLANs:'

Ограничение: Все задания надо выполнять используя только пройденные темы.
То есть эту задачу можно решить без использования условия if и циклов for/while.
"""

INT_MODE = input("Enter interface mode (access/trunk): ")
INT = input("Enter interface type and number: ")
ask_dict = {
    'access': 'Enter vlan number: ',
    'trunk': 'Enter allowed vlans: ',
}
print(ask_dict[INT_MODE])
VLANS = input()

config_dict = {
    'access': [
        'switchport mode access',
        'switchport access vlan {}',
        'switchport nonegotiate',
        'spanning-tree portfast',
        'spanning-tree bpduguard enable'
    ],
    'trunk': [
        'switchport trunk encapsulation dot1q',
        'switchport mode trunk',
        'switchport trunk allowed vlan {}'
    ]
}


print('\n' + '-' * 30)
print('interface {}'.format(INT))
print('\n'.join(config_dict[INT_MODE]).format(VLANS))
