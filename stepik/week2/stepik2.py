
import datetime
import itertools
import math
import simplecrypt
import os
import os.path
import shutil
import operator as op
from functools import partial


class NonPositiveError(Exception):
    pass


class PositiveList(list):
    def append(self, number) -> None:
        if number > 0:
            super(PositiveList, self).append(number)
        else:
            raise NonPositiveError


def datetime_after_delta():
    input_date = (int(i) for i in input().split())
    date = datetime.datetime(*input_date)
    input_delta = int(input())
    delta = datetime.timedelta(days=input_delta)
    result_date = date + delta
    print(result_date.year, result_date.month, result_date.day)


# перебрать пароли из файла passwords.txt и расшифровать файл encrypted.bin
def decrypt_file():
    with open("encrypted.bin", "rb") as inp:
        encrypted = inp.read()

    with open("passwords.txt") as passwords_file:
        passwords_raw = passwords_file.read()
        passwords = [password.strip() for password in passwords_raw.split()]
        for password in passwords:
            try:
                result = simplecrypt.decrypt(password, encrypted)
            except simplecrypt.DecryptionException:
                print(f'Wrong password {password}')
            else:
                print(f"Right password: {password}")
                with open(f"{password}.txt", "w") as file:
                    file.write(result.decode('utf8'))


class multifilter:

    def judge_half(self, pos: int, neg=0) -> bool:
        # допускает элемент, если его допускает хотя бы половина фукнций
        return pos >= neg

    def judge_any(self, pos: int, neg=0) -> bool:
        # допускает элемент, если его допускает хотя бы одна функция
        return pos >= 1

    def judge_all(self, pos: int, neg=0) -> bool:
        # допускает элемент, если его допускают все функции
        return neg == 0

    def __init__(self, iterable, *funcs, judge=judge_any):
        # iterable - исходная последовательность
        # funcs - допускающие функции
        # judge - решающая функция
        self.iterable = iterable
        self.funcs = funcs
        self.judge = judge

    def __iter__(self):
        # возвращает итератор по результирующей последовательности
        # print(self.judge.__name__, self.judge_any.__name__)
        for i in self.iterable:
            pos_neg = [f(i) for f in self.funcs]
            pos, neg = pos_neg.count(True), pos_neg.count(False)
            if self.judge(multifilter, pos, neg):
                yield i


def mul2(x):
    return x % 2 == 0

def mul3(x):
    return x % 3 == 0

def mul5(x):
    return x % 5 == 0

def multifilter_run():
    a = [i for i in range(31)]
    # [0, 1, 2, ... , 30]
    print(list(multifilter(a, mul2, mul3, mul5)))
    # [0, 2, 3, 4, 5, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 22, 24, 25, 26, 27, 28, 30]
    print(list(multifilter(a, mul2, mul3, mul5, judge=multifilter.judge_half)))
    # [0, 6, 10, 12, 15, 18, 20, 24, 30]
    print(list(multifilter(a, mul2, mul3, mul5, judge=multifilter.judge_all)))
    # [0, 30]


def primes():
    return (i for i in range(2, 10_000_000) if not (math.factorial(i-1)+1) % i)


source = "dataset_24465_4.txt"
reverse = "reverse.txt"
def reverse_file(source, reverse):
    with open(source) as source, open(reverse, "w") as result:
        data = source.read().splitlines()
        # for line in data[::-1]:
        #     result.write(f"{line}\n")
        data = "\n".join(data[::-1])
        result.write(data)


def os_practice():
    print(os.getcwd())
    print(os.listdir())
    print(os.path.exists("encrypted.bin"))
    print(os.path.isfile("readme.md"))
    print(os.path.isdir("readme.md"))
    print(os.path.abspath("stepik2.py"))
    os.chdir("C:\\Users\\junet\\PycharmProjects\\one\\stepik\\week1")
    print(os.getcwd())
    os.chdir("..")
    print(os.getcwd())
    print()

    for current_dir, dirs, files in os.walk("."):
        print(current_dir, dirs, files)


def copy_file(in_file, out_file):
    shutil.copy(in_file, out_file)


def copy_folder(in_foldr, out_folder):
    shutil.copytree(in_foldr, out_folder)


def find_all_python_dirs():
    """ Goes to ../main folder.
    Finds all directories with at least one .py file
    and writes paths to directories as sorted list in all_py_files_firs.txt"""
    all_python_dirs_list = []
    os.chdir("../main")
    root = os.getcwd().split('\\')[-1]  # get name of the root folder - "main"
    for current_dir, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".py"):
                all_python_dirs_list.append(root + current_dir[1:])
                break  # when first file is found - no need to check if any more .py files are in the directory
    all_python_dirs_list.sort()
    os.chdir("../week2")
    with open("all_py_files_dirs.txt", 'w') as f:
        data = "\n".join(all_python_dirs_list)
        f.write(data)


def mod_checker(x, mod=0):
    """ Возвращает лямбда функцию от одного аргумента y, которая будет возвращать True,
    если остаток от деления y на x равен mod, и False иначе."""
    return lambda y: op.mod(y, x) == mod


# example of using partial
x = int("1011", base=2)
int_base_2 = partial(int, base=2)
x = int_base_2("1011")


if __name__ == "__main__":
    # multifilter_run()
    # print(list(itertools.takewhile(lambda x : x <= 31, primes())))
    # reverse_file(source, reverse)
    # os_practice()
    # find_all_python_dirs()
    mod_3 = mod_checker(3)

    print(mod_3(3))  # True
    print(mod_3(4))  # False

    mod_3_1 = mod_checker(3, 1)
    print(mod_3_1(4))  # True
