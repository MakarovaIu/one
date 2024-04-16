###########################
# 6.00.2x Problem Set 1: Space Cows 

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

FILENAME = "ps1_cow_data.txt"
LIMIT = 10


def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """

    cow_dict = dict()
    with open(filename, 'r') as f:
        for line in f:
            line_data = line.split(',')
            cow_dict[line_data[0]] = int(line_data[1])
    return cow_dict


# Problem 1
def greedy_cow_transport(cows, limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    cows = {cow: value for cow, value in sorted(cows.items(), key=lambda item: item[1], reverse=True) if value <= limit}
    result = []
    while cows:
        total_weight = 0
        one_trip = []
        for cow in cows.keys():
            if total_weight < limit and (total_weight + cows[cow]) <= limit:
                one_trip.append(cow)
                total_weight += cows[cow]
        result.append(one_trip)
        for cow in one_trip:
            del cows[cow]
    return result


# Problem 2
def brute_force_cow_transport(cows, limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    best_trip = []
    for partition in get_partitions(cows.items()):
        for subpartition in partition:
            if sum((cow[1] for cow in subpartition)) > limit:
                break
        else:
            if not best_trip or len(partition) < len(best_trip):
                best_trip = partition
    res = []
    for trip in best_trip:
        one_trip = []
        for cow in trip:
            one_trip.append(cow[0])
        res.append(one_trip)
    return res


def brute_force_cow_transport_old(cows, limit=10):
    cows = cows.copy()
    best_sublist_count = len(cows)
    result = []

    for item in (get_partitions(cows.keys())):
        print(f"\nitem: {item}")
        limit_not_exceeded = True
        sub_list_count = 0

        while limit_not_exceeded:
            for sub_list in item:
                print(f"Sublist: {sub_list}")
                current_weight = 0
                sub_list_count += 1

                for name in sub_list:
                    current_weight += cows[name]
                    print(f"current weight: {current_weight}")
                if current_weight > limit:
                    print("breaking")
                    break
            else:
                if sub_list_count <= best_sublist_count:
                    best_sublist_count = sub_list_count
                    result = item
                    print(f"sublist count:{sub_list_count}")
                    print(f"result: {result}")
            limit_not_exceeded = False
    return result


# Problem 3
def compare_cow_transport_algorithms(filename=FILENAME, limit=LIMIT):
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    cows = load_cows(filename)
    limit = limit
    start = time.time()
    res = greedy_cow_transport(cows, limit)
    print(f"Greedy algorythm: {len(res)} trips, took {round(time.time()-start, 5)} seconds")
    start = time.time()
    res = brute_force_cow_transport(cows, limit)
    print(f"Brute force algorythm: {len(res)} trips, took {round(time.time()-start, 5)} seconds")


def list_of_lists_to_tuples_converter(lst):
    """ Converts a list of lists to a tuple of tuples. Elements in sublists are sorted. """
    res = []
    for sublist in lst:
        sublist.sort()
        res.append(tuple(sublist))
    return tuple(res)


def test_greedy(cows, limit, expected_result):
    """ We assume all cow names are unique. """
    res = list_of_lists_to_tuples_converter(greedy_cow_transport(cows, limit))
    expected_result = list_of_lists_to_tuples_converter(expected_result)
    print('Ok' if res == expected_result else 'Not ok')


def test_brute_force(cows, limit, expected_result):
    """ Brute force algorythm may give various combinations of trips,
    so we check if the number of trips is what we expect."""
    res = len(brute_force_cow_transport(cows, limit))
    print('Ok' if res == expected_result else 'Not ok')


"""
Here is some test data for you to see the results of your algorithms with. 
Do not submit this along with any of your answers. Uncomment the last two
lines to print the result of your problem.
"""
if __name__ == '__main__':
    cows = load_cows(FILENAME)
    limit = LIMIT

    TEST_COWS1 = {'Rose': 42, 'Betsy': 39, 'Starlight': 54, 'Luna': 41, 'Buttercup': 11, 'Abby': 28, 'Willow': 59, 'Coco': 59}
    TEST_LIMIT1 = 120
    TEST_RES1 = [['Coco', 'Willow'], ['Buttercup', 'Rose', 'Starlight'], ['Abby', 'Betsy', 'Luna']]
    TEST_RES_FROMFILE = [['Betsy'], ['Henrietta'], ['Herman', 'Maggie'], ['Oreo', 'Moo Moo'],
                         ['Millie', 'Milkshake', 'Lola'], ['Florence']]

    TEST_COWS2 = {"Jesse": 6, "Maybel": 3, "Callie": 2, "Maggie": 5}
    TEST_LIMIT2 = 10
    TEST_RES2 = 2

    # print({cow: value for cow, value in sorted(cows.items(), key=lambda item: item[1], reverse=True)})
    # print(greedy_cow_transport(cows, limit))
    # print(brute_force_cow_transport(cows, limit))
    compare_cow_transport_algorithms()

    test_greedy(TEST_COWS1, TEST_LIMIT1, TEST_RES1)
    test_greedy(cows, limit, TEST_RES_FROMFILE)
    test_brute_force(TEST_COWS2, TEST_LIMIT2, TEST_RES2)
    test_brute_force(cows, limit, 5)
