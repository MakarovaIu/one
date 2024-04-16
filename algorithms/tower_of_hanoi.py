def tower_of_hanoi(n: int, start: int, end: int) -> None:
    """ Moves n blocks from statr position to the end.
    Prints out every move.
    Blocks count from top to bottom, where 1 is the smallest and n is the largest. """
    assert type(n) is int and type(start) is int and type(end) is int, "Arguments need to be numbers"
    if n == 1:
        print(f"Move block 1 from {start} to {end}")
    else:
        other = 6 - (start + end)
        tower_of_hanoi(n - 1, start, other)
        print(f"Move block {n} from {start} to {end}")
        tower_of_hanoi(n - 1, other, end)


if __name__ == '__main__':
    tower_of_hanoi(4, 1, 3)
