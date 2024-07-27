"""
4. Оптимизация скрипта
Дан следующий скрипт на Python для обработки списка чисел.
Оптимизируйте его для повышения производительности.

Исходный скрипт
numbers = [i for i in range(1, 1000001)]
squares = []
for number in numbers:
squares.append(number ** 2)
Оптимизированный скрипт
"""
numbers = range(1, 1000001)
squares = [number**2 for number in numbers]
