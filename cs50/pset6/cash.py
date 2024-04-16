
import re
from timeit import timeit


class Cash:
    quarter = 25
    dime = 10
    nickel = 5
    penny = 1

    def __init__(self):
        self.change_owed = self.get_change_owed()

    @staticmethod
    def get_change_owed():
        while True:
            change_owed = input("Change owed in dollars:")
            if change_owed is None:
                return None
            if len(change_owed) > 0 and re.search(r"^[+-]?\d*(?:\.\d*)?$", change_owed)\
                    and 0 <= float(change_owed) <= 100:
                try:
                    return float(change_owed)
                except ValueError:
                    pass

    def convert_to_cents(self):
        change_owed = self.change_owed
        change_owed *= 100
        change_owed = round(change_owed)
        return change_owed

    def change_counter_by_while(self):
        change_owed = self.convert_to_cents()
        counter = 0
        while change_owed >= self.quarter:
            counter += 1
            change_owed -= self.quarter
        while change_owed >= self.dime:
            counter += 1
            change_owed -= self.dime
        while change_owed >= self.nickel:
            counter += 1
            change_owed -= self.nickel
        while change_owed >= self.penny:
            counter += 1
            change_owed -= self.penny
        return counter

    @property
    def change_counter_by_while_as_property(self):
        change_owed = self.convert_to_cents()
        counter, quarter_counter, dime_counter, nickel_counter, penny_counter = 0, 0, 0, 0, 0
        while change_owed >= self.quarter:
            counter += 1
            change_owed -= self.quarter
            quarter_counter += 1
        while change_owed >= self.dime:
            counter += 1
            change_owed -= self.dime
            dime_counter += 1
        while change_owed >= self.nickel:
            counter += 1
            change_owed -= self.nickel
            nickel_counter += 1
        while change_owed >= self.penny:
            counter += 1
            change_owed -= self.penny
            penny_counter += 1
        return counter, quarter_counter, dime_counter, nickel_counter, penny_counter

    def print_out_coin_info(self):
        counter, quarter_counter, dime_counter, nickel_counter, penny_counter = self.change_counter_by_while_as_property
        print(f"Coins: {counter}, of which\n"
              f"quarters: {quarter_counter}\n"
              f"dimes: {dime_counter}\n"
              f"nickels: {nickel_counter}\n"
              f"pennies: {penny_counter}\n")

    def change_counter_by_modulo(self):
        change_owed = self.convert_to_cents()
        counter = 0
        if (change_owed // self.quarter) > 0:
            counter += change_owed // self.quarter
            change_owed %= self.quarter
        if (change_owed // self.dime) > 0:
            counter += change_owed // self.dime
            change_owed %= self.dime
        if (change_owed // self.nickel) > 0:
            counter += change_owed // self.nickel
            change_owed %= self.nickel
        if (change_owed // self.penny) > 0:
            counter += change_owed // self.penny
            change_owed %= self.penny
        return counter


cash = Cash()
if __name__ == '__main__':
    cash.print_out_coin_info()


# print(timeit('cash.change_counter_by_while()', globals=globals(), number=100000))
# print(timeit('cash.change_counter_by_modulo()', globals=globals(), number=100000))
# print(timeit('cash.change_counter_by_while_as_property', globals=globals(), number=100000))
