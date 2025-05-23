"""
Перед вами программа, которая вычисляет квадратный корень из заданного числа. Она работает, но в ней полным-полно ошибок в стиле оформления. Ваша задача — найти все недочёты и исправить их.
Подсказка

Самым простым решением будет — скопировать код в редактор, проверить его линтером и исправить в соответствии с подсказками:
message — строка перенесена с помощью бэкслеша, так нельзя;
from math import * — импортирование всего содержимого модуля может привести к проблемам; лучше импортировать from math import sqrt;
import itertools — пакет импортирован, но не применяется;
во многих местах кода отсутствуют необходимые пробелы или стоят лишние;
между блоками кода неправильное количество пустых строк;
название функции написано в стиле CamelCase и не соответствует PEP8;
имя переменной Number не соответствует PEP8;
"Мы вычислили корень квадратный ..." — неконсистентные кавычки, в остальном коде применяются одинарные;
print f"Мы вычислили корень квадратный из введённого вами числа. Это будет:... — слишком длинная строка, надо переносить;
"" Вычисляет квадратный корень"" — докстринг оформлен не по PEP257;
все функции в коде должны сопровождаться докстрингами;
в f-строках не должно быть исполняемой логики, вынесите логику в отдельную переменную;
в коде не должно быть неиспользуемых переменных.
"""

from math import sqrt

message = ('Добро пожаловать в самую лучшую программу для вычисления '
          'квадратного корня из заданного числа')


def calc_sqrt(number: float) -> float:
    """Вычисляет квадратный корень."""
    return sqrt(number)


def calc(your_number: float):
    """Вычисляет квадратный корень из заданного числа."""
    if your_number <= 0:
        return
    sqrt_number = calc_sqrt(your_number)
    print (f'Мы вычислили квадратный корень из введённого вами числа.'
           f'Это будет: {sqrt_number}')


print(message)
calc(25.5)