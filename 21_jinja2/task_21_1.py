# -*- coding: utf-8 -*-
"""
Задание 21.1

Создать функцию generate_config.

Параметры функции:
* template - путь к файлу с шаблоном (например, "templates/for.txt")
* data_dict - словарь со значениями, которые надо подставить в шаблон

Функция должна возвращать строку с конфигурацией, которая была сгенерирована.

Проверить работу функции на шаблоне templates/for.txt и данных из файла data_files/for.yml.

"""

from jinja2 import Environment, FileSystemLoader
import yaml
import sys
sys.path.insert(0, 'C:/Users/snowowl/PycharmProjects/Natenka_python_tasks/21_jinja2/')

def generate_config(template, data_dict):
    env = Environment(loader=FileSystemLoader('C:/Users/snowowl/PycharmProjects/Natenka_python_tasks/21_jinja2/templates'),
                      trim_blocks=True,lstrip_blocks=True)
    templ = env.get_template(template)
    return templ.render(data_dict)

with open('C:/Users/snowowl/PycharmProjects/Natenka_python_tasks/21_jinja2/data_files/for.yml') as f:
    var = yaml.safe_load(f)
conf = generate_config('for.txt', var)
with open('task_21_1_result.txt', 'w') as f:
    f.write(conf)