# C(n, k) = C(n - 1, k) + C(n - 1, k - 1)
# C(n, 0) = 1
# if k > n: C(n, k) = 0

import time


def get_two_ints():
    n, k = map(int, input().split())


def combination(n, k):
    if k > n:
        c = 0
        return c
    if k == 0:
        c = 1
        return c
    return combination(n - 1, k) + combination(n - 1, k - 1)


namespaces = {'global': {'parent': None, 'vars': []}, }


def add_namespace(namespace, var):
    if namespace in namespaces.keys():
        namespaces[namespace]['vars'].append(var)
    else:
        namespaces[namespace] = {'parent': 'global', 'vars': [var]}


def create_namespace(namespace, parent):
    namespaces[namespace] = {'parent': parent, 'vars': []}


def get_parent(namespace, var):
    # if var is in current namespace
    if var in namespaces[namespace]['vars']:
        return namespace
    else:
        # we recursively search through vars in parent
        current_namespace = namespaces[namespace]['parent']
        # if var is not found
        if current_namespace is None:
            return None
        return get_parent(current_namespace, var)


def namespace_task():
    requests = int(input())
    for i in range(requests):
        command, namespace, var = input().split()
        if command == "create":
            create_namespace(namespace, var)
        if command == "add":
            add_namespace(namespace, var)
        if command == "get":
            print(get_parent(namespace, var))


class MoneyBox:
    def __init__(self, capacity):
        # вместимость копилки
        self.capacity = capacity

    def can_add(self, v):
        # True, если можно добавить v монет, False иначе
        return self.capacity >= v

    def add(self, v):
        if self.can_add(v):
            self.capacity -= v
            return self.capacity
        return False


class Buffer:
    def __init__(self):
        self.sequence = []

    def add(self, *a):
        # добавить следующую часть последовательности
        self.sequence += a
        while len(self.sequence) >= 5:
            print(sum(self.sequence[0:5]))
            del self.sequence[0:5]

    def get_current_part(self):
        # вернуть сохраненные в текущий момент элементы последовательности в порядке, в котором они были добавлены
        return self.sequence


class ExtendedStack(list):

    def sum(self):
        # операция сложения
        self.append(self.pop() + self.pop())

    def sub(self):
        # операция вычитания
        self.append(self.pop() - self.pop())

    def mul(self):
        # операция умножения
        self.append(self.pop() * self.pop())

    def div(self):
        # операция целочисленного деления
        self.append(self.pop() // self.pop())


def test():
    ex_stack = ExtendedStack([1, 2, 3, 4, -3, 3, 5, 10])
    ex_stack.div()
    assert ex_stack.pop() == 2
    ex_stack.sub()
    assert ex_stack.pop() == 6
    ex_stack.sum()
    assert ex_stack.pop() == 7
    ex_stack.mul()
    assert ex_stack.pop() == 2
    assert len(ex_stack) == 0


class Loggable:
    def log(self, msg):
        print(str(time.ctime()) + ": " + str(msg))


class LoggableList(list, Loggable):
    def append(self, obj):
        super(LoggableList, self).append(obj)
        self.log(obj)


if __name__ == "__main__":
    #
    # namespace_task()
    #
    # buf = Buffer()
    # buf.add(1, 2, 3)
    # buf.get_current_part()  # вернуть [1, 2, 3]
    # buf.add(4, 5, 6)  # print(15) – вывод суммы первой пятерки элементов
    # buf.get_current_part()  # вернуть [6]
    # buf.add(7, 8, 9, 10)  # print(40) – вывод суммы второй пятерки элементов
    # buf.get_current_part()  # вернуть []
    # buf.add(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)  # print(5), print(5) – вывод сумм третьей и четвертой пятерки
    # buf.get_current_part()  # вернуть [1]
    #
    # test()

    a = LoggableList()
    a.append('msg 1')
    a.append('msg 2')
    print(a)
