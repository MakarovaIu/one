""" Simple implementation of Caesar cypher. """
# test example
# letters = 'abcxyz'
# step1 = 1


def cypher(string, step):
    step = int(step) % 26
    list_of_ord_after_cypher = [ord(l) + step if (ord(l) + step) <= 122 else 96 + (ord(l) + step) % 122 for l in string]
    res = map(chr, list_of_ord_after_cypher)
    res = ''.join(res)
    return res


def decypher(string, step):
    step = int(step) % 26
    list_of_ord_after_cypher = [ord(l) - step if (ord(l) - step) >= 97 else 26 + (ord(l) - step) for l in string]
    res = map(chr, list_of_ord_after_cypher)
    res = ''.join(res)
    return res


if __name__ == '__main__':

    s = input().lower()
    stp = input()
    print(cypher(s, stp))
    print(decypher(s, stp))

    # print(cypher(letters, step1))
