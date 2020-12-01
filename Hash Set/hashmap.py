"""
Часть 2:
HashMap с использованием техники "кукушка"

Ключ -- int, значение -- string.
Оперативная память -- контейнер расширяется в rehash_ratio раз при невозможности заполнять контейнер

Методы:
1. insert(key, val) - вставка val по ключу key
2. remove(key) - удаление ключа key
3. get(key), [key] - доступ по ключу key
4. [key] = val - присваивание ключу key значения val

Атрибуты:
1. size - размер множества
2. capacity - используемая под ячейки память (в сумме в 2-х массивах)

Дополнительные возможности:
1. str(my_map) - конверитрование в строку, например, print(my_map)
2. key in set - проверка на наличие ключа:
3. len(my_map) - количество элементов
4. for el in my_map - итерирование по ключам в цикле
"""
import random


class HashMap:
    # rehash_ratio - коэффициент увеличения размера списка при рехеше
    def __init__(self, rehash_ratio=1.5):
        # размер каждого из 2-х списков (общее количество хранимых ячеек в 2 раза выше)
        self.__capacity = 5
        # во сколько раз увеличивать списки при рехеше
        self.rehash_ratio = rehash_ratio
        # количество добавленных элементов
        self.__size = 0
        # 2 листа, в которые добавляются элементы
        self.list = [[None] * self.__capacity, [None] * self.__capacity]
        # две хеш функции для листов
        self.hash = [lambda val: self.__hash_1(val) % self.__capacity,
                     lambda val: self.__hash_2(val) % self.__capacity]
        # инициализация параметров хеш функций
        self.__change_par()

    # Хеш для 1го листа
    def __hash_1(self, key):
        key ^= (key << self.par[0])
        key ^= (key >> self.par[1])
        key ^= (key << self.par[2])
        return key

    # Хеш для 2-го листа
    def __hash_2(self, key):
        key ^= (key << self.par[3])
        key ^= (key >> self.par[4])
        key ^= (key << self.par[5])
        return key

    # Изменение параметров хеш функций (в начале и при рехеше)
    def __change_par(self):
        self.par = random.sample(list(range(5, 18)), 6)

    # Рехеш
    # 1. Создание новых хеш функций
    # 2. Увеличение длины списков в rehash_ratio
    # 3. Добавление элемента add_el в список
    # 4. Новое размещение элементов по спискам
    def __rehash(self, add_el=None):
        # полный лист элементов (без None) + add_el
        full_list = list(filter(lambda x: x is not None, self.list[0] + self.list[1] + [add_el]))
        while True:
            # меняем параметры
            self.__change_par()
            # меняем запас в rehash_ratio раз
            self.__capacity = int(self.rehash_ratio * self.__capacity)
            # создание 2-х новых списков для размещения элементов
            self.list = [[None] * self.__capacity, [None] * self.__capacity]
            # добавление элементов в 2 списка
            for el in full_list:
                if self.__rehash_insert(el):
                    # __rehash_insert(el) вернуло True
                    # не удалось добавить элемент, нужен новый рехеш
                    # выходим из цикла добавления элементов, начинаем заново с начала цикла while
                    break
            else:
                # все элементы из full_list успешно вставлены
                # выходим из цикла и завершаем работу функции
                break

    # Вставка элемента при рехеше
    # 1. Возвращает False, если вставка успешна, не надо заново делать рехеш
    # 2. Возвращает True, если вставка не успешна, нужно сделать рехеш
    def __rehash_insert(self, pair):
        # проверка свободных мест в 2-х списках
        for pos in random.sample([0, 1], 2):
            hash_key = self.hash[pos](pair[0])
            if self.list[pos][hash_key] is None:
                # свободное место
                self.list[pos][hash_key] = pair
                return False  # вставка успешна, рехеш не нужен

        # и слева, и справа ячейки заняты, начинаем перекидывать элементы
        # сохраняем начальную пару и её позицию, чтобы потом понять, когда мы зациклились
        first_pos = pos = random.choice([0, 1])
        first_pair = pair
        # вставляем начальную пару на место new_pair
        hash_key = self.hash[pos](pair[0])
        new_pair = self.list[pos][hash_key]
        self.list[pos][hash_key] = pair
        # теперь текущая пара - new_pair
        pair = new_pair
        # теперь позиция для вставки в другом списке
        pos = 1 - pos

        # пока мы не вернемся в начальную пару (т. е. пока не зациклимся), выполняем цикл
        while pair != first_pair or pos != first_pos:
            # проверка на свободное место
            hash_key = self.hash[pos](pair[0])
            if self.list[pos][hash_key] is None:
                # свободное место
                self.list[pos][hash_key] = pair
                return False  # вставка успешна, рехеш не нужен
            # вставляем pair на место new_pair
            new_pair = self.list[pos][hash_key]
            self.list[pos][hash_key] = pair
            # теперь текущая пара - new_pair
            pair = new_pair
            pos = 1 - pos
        # вышли из цикла (пришли в начальную позицию)
        return True  # элемент не вставлен, нужен повторный рехеш

    # Обычная вставка
    def insert(self, key, val):
        pair = (key, val)
        # проверка на наличие добавляемого ключа в списке (изменение значения для ключа)
        for pos in random.sample([0, 1], 2):
            hash_key = self.hash[pos](key)
            if self.list[pos][hash_key] is not None and self.list[pos][hash_key][0] == key:
                # замена старого значения по ключу на новое
                self.list[pos][hash_key] = pair
                return
        # элемента с таким ключём не было, т. е. элемент - новый
        self.__size += 1
        # проверка свободных мест в 2 списках
        for pos in random.sample([0, 1], 2):
            hash_key = self.hash[pos](key)
            if self.list[pos][hash_key] is None:
                # свободное место
                self.list[pos][hash_key] = pair
                return

        # и слева, и справа ячейки заняты, начинаем тасовать элементы
        # сохраняем начальную пару и её позицию, чтобы потом понять, когда мы зациклились
        first_pos = pos = random.choice([0, 1])
        first_pair = pair
        # вставляем начальную пару на место new_pair
        hash_key = self.hash[pos](pair[0])
        new_pair = self.list[pos][hash_key]
        self.list[pos][hash_key] = pair
        # теперь текущая пара - new_pair
        pair = new_pair
        # позиция для вставки в другом списке
        pos = 1 - pos

        # пока мы не вернемся в начальную пару на начальной позиции (т. е. пока не зациклимся), выполняем цикл
        while new_pair[0] != first_pair[0] or pos != first_pos:
            # проверка на свободное место
            hash_key = self.hash[pos](pair[0])
            if self.list[pos][hash_key] is None:
                # свободное место
                self.list[pos][hash_key] = pair
                return
            # вставляем pair на место new_pair
            new_pair = self.list[pos][hash_key]
            self.list[pos][hash_key] = pair
            # теперь текущая пара - new_pair
            pair = new_pair
            pos = 1 - pos
        # вышли из цикла (пришли в начальную позицию)
        # нужен рехеш с добавлением текущей пары pair
        self.__rehash(pair)

    # Удаление элемента
    # 1. Возвращает значение по ключу, если ключ есть
    # 2. Возвращает None, если ключа нет
    def remove(self, key):
        # провека на наличие ключа в 2-х списках
        for pos in random.sample([0, 1], 2):
            hash_key = self.hash[pos](key)
            pair = self.list[pos][hash_key]
            if pair is not None and pair[0] == key:
                # ключ найден, удаляем его
                self.list[pos][hash_key] = None
                self.__size -= 1
                return pair[1]  # возвращаем значение по ключу
        # ключ не найден, возвращаем None

    # Получение элемента по ключу
    # 1. Возвращает значение по ключу, если такой ключ был
    # 2. Возвращает None, если ключа не было
    def __getitem__(self, key):
        # проверка на наличие добавляемого ключа в списке
        for pos in random.sample([0, 1], 2):
            hash_key = self.hash[pos](key)
            pair = self.list[pos][hash_key]
            if pair is not None and pair[0] == key:
                return pair[1]  # ключ найден
        # ключ не найдем, возвращаем None

    # Метод get возвращает значение по ключу, эквивалентен методу __getitem__()
    def get(self, key):
        return self.__getitem__(key)

    # Присваивание по ключу - обычная вставка
    def __setitem__(self, key, value):
        self.insert(key, value)

    # Дополнительные методы:

    # Проверка на наличие ключа
    def __contains__(self, key):
        # проверяем наличие в 2-х списках
        for pos in random.sample([0, 1], 2):
            hash_key = self.hash[pos](key)
            pair = self.list[pos][hash_key]
            if pair is not None and pair[0] == key:
                # ключ найден
                return True
        # ключ не найден
        return False

    # Строковое представление
    # Выводит в {} скобках через запятую пары key: 'value'
    def __str__(self):
        return '{' + ', '.join(
            list(map(
                lambda pair: "{}: '{}'".format(*pair), filter(lambda x: x is not None, self.list[0])
            )) +
            list(map(
                lambda pair: "{}: '{}'".format(*pair), filter(lambda x: x is not None, self.list[1])
            ))
        ) + '}'

    # Количество элементов в HashMap
    @property
    def size(self):
        return self.__size

    # Общий размер 2-х выделенных списков (используемая память)
    @property
    def capacity(self):
        return self.__capacity * 2

    # Длина HashMap - эквивалентна свойству size
    def __len__(self):
        return self.__size

    # Итерирование в цикле for
    def __iter__(self):
        return HashSetIterator(self.list)


# Итератор
class HashSetIterator:
    def __init__(self, lists):
        # текущий лист
        self.curr_list = 0
        # filter-итераторы для каждого из листов без None
        self.list = list(map(lambda i:
                             filter(lambda x: x is not None, lists[i]), [0, 1]))

    def __next__(self):
        # если это 2-й лист, то возвращаем следующий элемент
        # если это последний элемент во 2-м листе, то filter выбросит StopIteration
        if self.curr_list == 1:
            return next(self.list[1])[0]
        # если это 1-й лист, то нужно поймать StopIteration от filter, чтобы перейти ко 2-му листу
        try:
            return next(self.list[0])[0]
        except StopIteration:
            # переход ко 2-му листу
            self.curr_list = 1
            return self.__next__()
