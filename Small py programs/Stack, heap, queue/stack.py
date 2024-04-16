def main():
    stack = []
    while user_input := input():
        match user_input.split():
            case 'add', num:
                stack.append(int(num))
            case 'head', :
                print(stack[-1])
            case 'pop', :
                print(stack.pop())
            case 'close', :
                break


if __name__ == '__main__':
    main()
