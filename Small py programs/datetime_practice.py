import calendar
from datetime import datetime


def get_dates():
    date1 = input()
    date2 = input()
    date1 = datetime.strptime(date1, "%Y-%m-%d")
    date2 = datetime.strptime(date2, "%Y-%m-%d")
    return date1, date2


def main(date1, date2):
    if date1.month != date2.month:
        days_in_month = calendar.monthrange(date1.year, date1.month)[-1]
        end_date = datetime(year=date1.year, month=date1.month, day=days_in_month)
        delta = (end_date - date1).days + 1
    else:
        delta = (date2 - date1).days + 1
    return delta


if __name__ == '__main__':
    dt1, dt2 = get_dates()
    result = main(dt1, dt2)
    print(result)
