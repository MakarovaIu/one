from collections import Counter
from collections import OrderedDict


class SimpleLogParser:
    def __init__(self):
        self.requests = []
        self.http_codes = []
        self.req_res = None
        self.http_codes_res = None

    def get_input(self):
        while (user_input := input()) != 'end':
            request, http_code = user_input.split(' ')
            self.requests.append(request)
            self.http_codes.append(http_code)

    def parse_data(self):
        req_res_counter = Counter(self.requests)
        http_codes_res_counter = Counter(self.http_codes)
        self.req_res = OrderedDict(sorted(req_res_counter.items()))
        self.http_codes_res = OrderedDict(sorted(http_codes_res_counter.items()))

    def print_output(self):
        for key, val in self.http_codes_res.items():
            print(key, val)
        for key, val in self.req_res.items():
            print(key, val)

    def main(self):
        self.get_input()
        self.parse_data()
        self.print_output()


if __name__ == '__main__':
    SimpleLogParser().main()
