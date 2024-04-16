import heapq


def main():
    heap = [-int(i) for i in input().split()]
    heapq.heapify(heap)
    while user_input := input():
        match user_input.split():
            case 'insert', num:
                heapq.heappush(heap, -int(num))
            case 'pop', :
                print(-(heapq.heappop(heap)))
            case 'end', :
                break


if __name__ == '__main__':
    main()
