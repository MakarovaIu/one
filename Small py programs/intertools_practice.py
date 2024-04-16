from itertools import groupby

# test data
# data = [('США', 'Нью-Йорк'),
#         ('Россия', 'Краснодар'),
#         ('Нидерланды', 'Амстердам'),
#         ('Россия', 'Москва'),
#         ('США', 'Вашингтон'),
#         ]


def getting_data():
    data = []
    inputs_num = input()
    for _ in range(int(inputs_num)):
        city, country = input().split()
        data.append((country, city))
    return data


def main(data):
    data.sort()
    grouped_data = groupby(data, key=lambda x: x[0])
    new_data = []
    for country, cities in grouped_data:
        for city in list(cities):
            new_data.append(f"{country} {city[1]}")
        new_data.append("<->")

    for item in new_data[:-1]:
        print(item)


if __name__ == '__main__':
    dataset = getting_data()
    main(dataset)
