class CountingBot:
    def __init__(self):
        self.number = 0
        self.user_number = None
        self.command = None
        self.counting_on = True

    def get_user_input(self):
        user_input = input().split()
        self.command = user_input[0]
        if len(user_input) == 2:
            try:
                self.user_number = int(user_input[1])
            except ValueError:
                print("Wrong input. Integer number needed")

    def main(self):
        while self.counting_on:
            self.get_user_input()
            match self.command:
                case 'zero':
                    self.number = 0
                case 'add':
                    self.number += self.user_number
                case 'minus':
                    self.number -= self.user_number
                case 'mul':
                    self.number *= self.user_number
                case 'div':
                    if not self.user_number:
                        print("Can't divide by zero")
                        continue
                    self.number //= self.user_number
                case 'result':
                    print(self.number)
                case 'exit':
                    self.counting_on = False
                case _:
                    print("Wrong command")


if __name__ == '__main__':
    prog = CountingBot()
    prog.main()
