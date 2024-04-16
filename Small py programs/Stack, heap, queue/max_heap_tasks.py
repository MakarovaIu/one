import heapq


def main():
    heap = []
    while user_input := input():
        match user_input.split():
            case 'task', task:
                task = task.split(',')
                heapq.heappush(heap, (-int(task[1]), -int(task[0])))
            case 'take', :
                task_to_pop = heapq.heappop(heap)
                print(f"Задача {-task_to_pop[1]} с приоритетом {-task_to_pop[0]}")
            case 'end', :
                break


if __name__ == '__main__':
    main()
