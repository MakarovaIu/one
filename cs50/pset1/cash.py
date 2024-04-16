# --- !!! ---
# Keep tkwindow.py the same directory as cash.py

# --- About ---
# Implements a small program with GUI to demonstrate the greedy algorithm
# This is the optimal algorithm to count minimum amount of coins needed to represent dollars and cents
# The solution is made for sum in dollars, where quarter, dime, nickel and pennie are 25, 10, 5 and 1 cents respectively

# --- To use ---
# Print the amount in dollars in the window using only digits and dot notation.
# Anything smaller than a cent won't count, rounding money only down
# Press "enter" or the button "Let's go" to see the result

from tkwindow import TKWindow
import decimal


class Cash:
    coins = {"QUARTER": 25, "DIME": 10, "NICKEL": 5, "PENNIE": 1}

    def __init__(self, change):
        change = change.rstrip("$")
        if Cash.input_check(change):
            self.change_owed = Cash.convert_to_cents(decimal.Decimal(change))
        else:
            raise ValueError
        self.change = {"quarter": 0, "dime": 0, "nickel": 0, "pennie": 0}
        self.coin_counter = 0

    @property
    def change_owed(self):
        return self._change_owed

    @change_owed.setter
    def change_owed(self, change):
        self._change_owed = change

    @staticmethod
    def get_input_from_console():
        while True:
            change_owed = input("Change owed:\n")
            if Cash.input_check(change_owed):
                return str(change_owed)
            else:
                print("Please enter amount in dollars")

    @staticmethod
    def console_implementation():
        cash = Cash(Cash.get_input_from_console())
        print(cash.output_func())

    @staticmethod
    def input_check(changed_owed):
        try:
            if float(changed_owed) >= 0:
                return True
        except ValueError:
            return False

    @staticmethod
    def convert_to_cents(change):
        return int(change * 100)

    def count_change(self):
        change_owed = self.change_owed
        for coin in self.coins.items():
            if change_owed >= coin[1]:
                counter, change_owed = divmod(change_owed, coin[1])
                self.coin_counter += counter
                self.change[coin[0].lower()] = counter

    def output_func(self):
        self.count_change()
        return f"You have {decimal.Decimal(self.change_owed) / 100} dollars.\n" \
               f"It takes minimum {int(self.coin_counter)} coins.\n" \
               f"quarters : {self.change['quarter']}\n" \
               f"dimes    : {self.change['dime']}\n" \
               f"nickels  : {self.change['nickel']}\n" \
               f"pennies  : {self.change['pennie']}\n"


title = "Greedy"
label1 = "\nHere is a greedy game.\n"
label2 = "Enter your cash in dollars to see the fewest coins possible to make it.\n"\
         "Use dot notation for cents."
errormsg = "Please enter dollars\n" \
           "with digits and dot notation\n" \
           "if needed."
classname = Cash
func = "output_func"

if __name__ == "__main__":

    # Cash.console_implementation()
    TKWindow(title, label1, label2, errormsg, classname, func)
