# You are given numbers in a file.
# If there is a math fact about this number you get "Interesting" output else "Boring".
# Answers are given the same order the numbers are input.

from pprint import pprint
import requests


class InterestingNumbers:
    def __init__(self):
        self.numbers = {}
        self.api_url = "http://numbersapi.com/{}/math?json=true"

    def read_file(self, file):
        """ Reads the file and stores numbers as keys in self.numbers dict with "Boring" value as default.
         Assumes it's python >3.6 and dict is ordered. """
        with open(file) as file:
            for number in file:
                self.numbers[number.rstrip()] = "Boring"

    def check_numbers(self):
        """ For every number if there is a math fact about it
        changes its state in the self.numbers dict to 'Interesting'. """
        for number in self.numbers.keys():
            res = requests.get(self.api_url.format(number), timeout=3)
            num_json = res.json()
            # pprint(num_json)
            if num_json['found']:
                self.numbers[number] = "Interesting"

    def print_number_facts(self):
        for fact in self.numbers.values():
            print(fact)

    def main(self, file_name):
        self.read_file(file_name)
        self.check_numbers()
        self.print_number_facts()


if __name__ == '__main__':
    f = "numbers.txt"

    e = InterestingNumbers()
    e.main(f)
