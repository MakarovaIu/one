# --- !!! ---
# Keep tkwindow.py the same directory as credit.py

# --- About ---
# A small program with GUI
# Determines if the credit card number is valid and what company it belongs to
# Supported types: American Express, Visa, Mastercard

# --- To use ---
# Enter a credit card number
# You can find number examples at:
# https://developer.paypal.com/docs/payflow/payflow-pro/payflow-pro-testing/#credit-card-numbers-for-testing

from tkwindow import TKWindow


class CreditCard:
    def __init__(self, card=None):
        if not card:
            card = CreditCard.get_input()
        self.card = str(card)

    @property
    def card(self):
        return self._card

    @card.setter
    def card(self, card):
        if CreditCard.validate_input(card):
            self._card = card
        else:
            raise ValueError

    @staticmethod
    def get_input():
        while True:
            card = input("Enter card number: ")
            if CreditCard.validate_input(card):
                return card
            else:
                print("Use only digits")

    @staticmethod
    def validate_input(card):
        try:
            int(card)
            return True
        except ValueError:
            return False

    def get_digits_sum(self):
        reverse_card = self.card[::-1]
        sec_sum_card = reverse_card[1::2]
        second_digits_sum = []
        for num in sec_sum_card:
            num = int(num) * 2
            if num >= 10:
                num = sum((int(digit) for digit in str(num)))
            second_digits_sum.append(num)
        return sum(second_digits_sum) + sum(int(num) for num in reverse_card[::2])

    def validate_card(self):
        if self.get_digits_sum() % 10 == 0:
            return True
        return False

    def output_func(self):
        if self.validate_card():
            if len(self.card) == 15 and self.card.startswith(("34", "37")):
                return "American Express"
            elif len(self.card) == 16 and self.card.startswith(("51", "52", "53", "54", "55", "2")):
                return "Mastercard"
            elif (len(self.card) == 13 or len(self.card) == 16) and self.card.startswith("4"):
                return "Visa"
            else:
                return "Unknown company"
        else:
            return "Not a valid card"


title = "Credit Cards"
label1 = None
label2 = "Enter credit card number as only digits\n" \
         "to see if it's valid and what company it is"
errormsg = "Please enter a card number"
classname = CreditCard
func = "output_func"
link = "https://developer.paypal.com/docs/payflow/payflow-pro/payflow-pro-testing/#credit-card-numbers-for-testing"

if __name__ == "__main__":
    TKWindow(title, label1, label2, errormsg, classname, func, link)
