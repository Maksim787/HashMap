# Тест добавляет случайные n элементов, а потом удаляет случайные n // 10 элементов
# При рехеше проверяется объем занятой памяти до рехеша (в среднем 50% при данной реализации)
# Все операции проверяются на корректность


from hashmap import *
import random

random.seed(1)
rehash_ratio = 1.5
# наш словарь
my_map = HashMap(rehash_ratio)
# настоящий словарь для проверки
true_map = {}

n = 50000  # Число элементов для вставки
curr_capacity = my_map.capacity
curr_size = my_map.size

for i in range(n):
    # случайный элемент для вставки
    integer = random.randint(-214748368, 214748367)
    string = "Значение от {}".format(integer)

    my_map[integer] = string
    true_map[integer] = string

    # проверка на рехеш
    if my_map.capacity != curr_capacity:
        print("Рехеш при {} элементах ({:0.2f}% заполненность)".format(curr_size, curr_size * 100 / curr_capacity))
        print("Изменение capacity с {} до {}".format(curr_capacity, my_map.capacity))
        print()

    curr_size = my_map.size
    curr_capacity = my_map.capacity

    # проверка размеров
    assert len(true_map) == len(my_map)
    # проверка корректности добавления
    assert integer in my_map
    # проверка корректности значения по ключу
    assert my_map[integer] == string

# проверка на то, что true_map содержится в my_map
for key in true_map:
    assert key in my_map and my_map[key] == true_map[key]
# проверка на то, что my_map содержится в true_map
for key in my_map:
    assert key in true_map and my_map[key] == true_map[key]

# случайные n // 10 элементов для удаления
remove_el = random.sample(sorted(true_map), n // 10)
for el in remove_el:
    my_map.remove(el)
    true_map.pop(el)
    # проверка на размер
    assert len(true_map) == len(my_map)
    # проверка на корректность удаления
    assert el not in my_map

# проверка на коррестность удаления
for el in remove_el:
    assert el not in my_map
# проверка на то, что true_map содержится в my_map
for el in true_map:
    assert el in my_map and my_map[el] == true_map[el]
# проверка на то, что my_map содержится в true_map
for el in my_map:
    assert el in true_map and my_map[el] == true_map[el]

# # Снизить n до 5-10 и убрать комментарии
# # Печать словарей
# print(true_map)
# print(my_map)
# # Итерация по словарю
# for key in my_map:
#     print("{}: '{}'".format(key, my_map[key]), end=', ')
# print()

print("No errors")
