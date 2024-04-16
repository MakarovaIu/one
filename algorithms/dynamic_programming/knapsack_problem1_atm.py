"""
Задача Банкомат.
В банкомате банкноты различных номиналов. Нужно выдать сумму TOTAL, используя минимальное количество купюр.
Пусть F[k]- минимальное число банкнот, при помощи которых можно выдать сумму в k рублей.
Выберем одну из банкнот, входящую в оптимальный способ выдачи. Пусть это банкнота b[i].
Тогда необходимо выдать оставшуюся сумму k-b[i], что можно сделать при помощи F[k-b[i]] банкнот.
То есть F[k] = 1 + F[k-b[i]]
Далее необходимо взять минимум по всем возможным значениями: F[k] = 1 + min[i](F[k-b[i]]).
Начальные значения удобно сделать такими: F[0]=0, F[k]=inf, k>0.
Значение inf будет означать невозможность выдачи суммы вообще.
Рассматриваются только такие значения k и i, когда k>=b[i].
Номиналы банкнот хранятся в спискe list_of_banknotes и нумерация банкнот начинается с числа 0.
"""

TOTAL = 3
list_of_banknotes = [2, 5, 8, 25, 40]
inf = float("inf")
min_number_of_banknotes = [inf] * (TOTAL + 1)
# index is the money to give, value is the minimum number of banknotes to give the money.
min_number_of_banknotes[0] = 0

# перебираем каждую целую сумму от 1 до TOTAL
for money_to_give in range(1, TOTAL + 1):
    # перебираем каждую банкноту из доступных
    for banknote in list_of_banknotes:
        # если сумма больше или равно банкноте и остаток суммы выражается через меньшее число, чем сумма
        if money_to_give >= banknote \
                and min_number_of_banknotes[money_to_give - banknote] < min_number_of_banknotes[money_to_give]:
            # то сумма выражается через то же число, что и сумма - банкнота (+1 добавим позже)
            min_number_of_banknotes[money_to_give] = min_number_of_banknotes[money_to_give - banknote]
    # перебрав все банкноты к текущей сумме и тем самым найдя минимальное количество банкнот
    # для выражения сумма - банкнота, прибавляем к счётчику 1
    min_number_of_banknotes[money_to_give] += 1
print(min_number_of_banknotes)

"""
Для восстановления ответа будем опять идти «к началу» списка, уменьшая сумму money_to_give, 
выбирая такую банкноту banknote, что 
min_number_of_banknotes[money_to_give] = min_number_of_banknotes[money_to_give - banknote] + 1. 
Номиналы банкнот, которые будут при этом использоваться для восстановления ответа, будут записаны в список Ans.
"""

Ans = []
money_to_give = TOTAL
while money_to_give != 0:
    if min_number_of_banknotes[money_to_give] == inf:
        Ans.append(f"Banknotes to give {money_to_give} are not available.")
        break
    for banknote in list_of_banknotes:
        if money_to_give >= banknote and \
                min_number_of_banknotes[money_to_give] == min_number_of_banknotes[money_to_give - banknote] + 1:
            Ans.append(banknote)
            money_to_give -= banknote
print(Ans)
