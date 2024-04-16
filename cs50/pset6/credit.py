class Credit:

    def __init__(self):
        self.credit_card = self.get_input()

    def get_input(self):
        while True:
            user_input = input("Credit card number: ")
            if self.input_validation(user_input):
                return user_input

    @staticmethod
    def input_validation(user_input):
        if not user_input.isdigit():
            print("Not a credit card number, please try again.")
            return False
        return True

    def input_reverse(self):
        credit_card = self.credit_card[::-1]
        return credit_card

    def every_second_digits_sum(self):
        credit_card = self.input_reverse()
        second_digits_sum = 0
        res_list = []
        for number in credit_card[1::2]:
            res = int(number) * 2
            if res >= 10:
                res = str(res)
                res = int(res[0]) + int(res[1])
            res_list.append(res)
        for i in res_list:
            second_digits_sum += i
        return second_digits_sum

    def other_digits_sum(self):
        credit_card = self.input_reverse()
        other_digits_sum = 0
        for number in credit_card[::2]:
            other_digits_sum += int(number)
        return other_digits_sum

    def check_card_is_valid(self):
        if (self.every_second_digits_sum() + self.other_digits_sum()) % 10 == 0:
            if len(self.credit_card) == 15 and self.credit_card.startswith(("34", "37")):
                print("Amex")
            elif len(self.credit_card) == 16 and self.credit_card.startswith(("51", "51", "53", "54", "55")):
                print("MasterCard")
            elif (len(self.credit_card) == 13 or len(self.credit_card) == 16) and self.credit_card.startswith("4"):
                print("Visa")
            else:
                print("None of the above")
            return True
        print("Not valid")

    # def card_company(self):
    #     if self.check_card_is_valid():


credit = Credit()
print(credit.every_second_digits_sum())
print(credit.other_digits_sum())
credit.check_card_is_valid()
a = 4149538613119877
