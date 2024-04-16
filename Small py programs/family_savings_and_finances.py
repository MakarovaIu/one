from decimal import Decimal, ROUND_HALF_EVEN

VACATION_PERCENT = 10
FOOD_PERCENT = 30
RENT_PERCENT = 5
HOBBY_PERCENT = 15
REST = 100 - VACATION_PERCENT - FOOD_PERCENT - RENT_PERCENT - HOBBY_PERCENT


def category_money(init_money: Decimal, percent: int | float) -> Decimal:
    """ returns money in cents """
    percent = Decimal(f"{percent:.2f}")
    return init_money * percent


def money_left(cat_money: Decimal):
    """ returns rest money left less than 1 cent """
    return cat_money - int(cat_money)


def main():
    """ gets user input of 2 salaries and returns answer with money data on each savings category """
    m1 = Decimal(input("Зарплата члена семьи №1"))
    m2 = Decimal(input("Зарплата члена семьи №2"))
    money = m1 + m2

    vacation = category_money(money, VACATION_PERCENT)
    food = category_money(money, FOOD_PERCENT)
    rent = category_money(money, RENT_PERCENT)
    hobby = category_money(money, HOBBY_PERCENT)
    cents_left = money_left(vacation) + money_left(food) + money_left(rent) + money_left(hobby)
    rest = (category_money(money, REST) + cents_left).quantize(Decimal("1.00"))

    answer = f"Отпуск: {vacation // 100} руб. {int(vacation) % 100} коп.\n" \
             f"Пропитание и еда: {food // 100} руб. {int(food) % 100} коп.\n" \
             f"Коммунальные платежи: {rent // 100} руб. {int(rent) % 100} коп.\n" \
             f"Досуг: {hobby // 100} руб. {int(hobby) % 100} коп.\n" \
             f"Накопления: {rest // 100} руб. {int(rest) % 100} коп.\n"

    return answer


if __name__ == '__main__':
    print(main())
