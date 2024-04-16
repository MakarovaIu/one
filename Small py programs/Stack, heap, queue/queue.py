from collections import deque


def main():
    queue = deque()
    while user_input := input():
        match user_input.split():
            case 'add', num:
                queue.appendleft(int(num))
            case 'head', :
                print(queue[-1])
            case 'pop', :
                print(queue.pop())
            case 'close', :
                break


if __name__ == '__main__':
    main()
