"""
b0 - the amount you owe a bank in month 0
p0 - the amount you pay a bank in month 0
ub0 - unpaid balance in month 0
ub0 = b0 - p0
r - annual interest rate
mp - minimum payment
b1 - the amount you owe a bank in month 1
b1 is equal to your unpaid balance plus interest on your unpaid balance
b1 = ub0 + r/12 * ub0
ub1 = b1 - p1
b2 = ub1 + r/12 * ub1
"""


def balance_with_minimum_monthly_payment(balance=42, monthly_payment_rate=0.04, annual_interest_rate=0.2):
    """ what is left to pay in 12 months when you pay only minimum monthly payment """
    for month in range(1, 13):
        fixed_minimum_monthly_payment = monthly_payment_rate * balance
        monthly_unpaid_balance = balance - fixed_minimum_monthly_payment
        balance = monthly_unpaid_balance + annual_interest_rate/12 * monthly_unpaid_balance
    return round(balance, 2)


print("Remaining balance: ", balance_with_minimum_monthly_payment())


def minimum_monthly_payment(initial_balance):
    """ minimum fixed payment to close your debt in 12 months """
    minimum_monthly_fixed_payment = 0
    balance = initial_balance
    while balance > 0:
        minimum_monthly_fixed_payment += 10
        balance = calculate_balance(initial_balance, minimum_monthly_fixed_payment)
    return minimum_monthly_fixed_payment


def calculate_balance(balance, minimum_monthly_fixed_payment, annual_interest_rate=0.2):
    """ tells your debt after 12 months """
    for month in range(1, 13):
        monthly_unpaid_balance = balance - minimum_monthly_fixed_payment
        balance = monthly_unpaid_balance + annual_interest_rate/12 * monthly_unpaid_balance
    return balance


print(minimum_monthly_payment(3329))


def minimum_monthly_payment_recur(start_balance, annual_interest_rate):
    """ finding optimal monthly payment to close your debt in a year """
    lower_bound = start_balance/12
    upper_bound = (start_balance * ((1 + annual_interest_rate/12)**12))/12

    def minimum_monthly_payment_subreccursion(balance, lower, upper):
        """ recursively checks if monthly payment is enough to make balance 0 """
        monthly_payment = (lower + upper)/2
        initial_balance = balance
        for month in range(12):
            monthly_unpaid_balance = balance - monthly_payment
            balance = monthly_unpaid_balance + annual_interest_rate / 12 * monthly_unpaid_balance
        if abs(balance) < 0.01:
            return round(monthly_payment, 2)
        if balance > 0:
            return minimum_monthly_payment_subreccursion(initial_balance, monthly_payment, upper)
        if balance < 0:
            return minimum_monthly_payment_subreccursion(initial_balance, lower, monthly_payment)

    return minimum_monthly_payment_subreccursion(start_balance, lower_bound, upper_bound)


print(minimum_monthly_payment_recur(999999, 0.18))

'''
minimum_fixed_payment = 0
balance = 4773
annual_interest_rate = 0.2
while balance > 0:
    balance = 4773
    minimum_fixed_payment += 10
    for month in range(1, 13):
        monthly_unpaid_balance = balance - minimum_fixed_payment
        balance = monthly_unpaid_balance + annual_interest_rate/12 * monthly_unpaid_balance
print(minimum_fixed_payment)
'''