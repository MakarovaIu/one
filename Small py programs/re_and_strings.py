""" Программа принимает на вход строку, заменяет символы на другую раскладку клавиатуры и выводит на экран.
 En -> Ru, Ru -> En """

import re

ru = "йцукенгшщзхъфывапролджэячсмитьбю.ё\"№;:?"
en = "qwertyuiop[]asdfghjkl;'zxcvbnm,./`@#$^&"

ru_to_en = dict(zip(ru, en))
en_to_ru = dict(zip(en, ru))

user_input = input().lower()

if re.search(r"[a-z]+", user_input):
    table = user_input.maketrans(en_to_ru)
else:
    table = user_input.maketrans(ru_to_en)
print(user_input.translate(table))
