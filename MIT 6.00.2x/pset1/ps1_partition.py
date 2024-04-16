# From codereview.stackexchange.com
def partitions(set_, toPrint=False):
    if not set_:
        if toPrint: print("empty set")
        yield []
        return
    for i in range(2 ** len(set_) // 2):
        parts = [set(), set()]
        if toPrint: print(f"{i=}, {bin(i)=}, {parts=}")
        for item in set_:
            parts[i & 1].add(item)
            if toPrint: print(parts, bin(i), i)
            i >>= 1
        if toPrint: print(f"{parts[1]=}")
        for b in partitions(parts[1], toPrint):
            if toPrint: print(f"{parts[0]=}, {parts[1]=}")
            if toPrint: print(f"{[parts[0]] + b=}")
            yield [parts[0]] + b


# This is a helper function that will fetch all of the available 
# partitions for you to use for your brute force algorithm.
def get_partitions(set_, toPrint=False, toPrintOuter=False):
    for partition in partitions(set_, toPrint):
        if toPrintOuter: print("yielding from outer func")
        yield [list(elt) for elt in partition]


# Uncomment the following code  and run this file to see what get_partitions does if you want to visualize it:
if __name__ == '__main__':

    for item in (get_partitions(['a', 'b', 'c', 'd'], toPrint=False, toPrintOuter=False)):
        print(item)
