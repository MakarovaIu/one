import csv
from collections import Counter
import json
import requests


def most_common_crime_2015():
    with open("crimes.csv") as f:
        reader = csv.DictReader(f)
        crimes = []
        for row in reader:
            if "2015" in row["Date"]:
                crimes.append(row["Primary Type"])
        res = Counter(crimes).most_common(1)
        print(res[0][0])


data = [{
    'hostname': 'sw1',
    'location': 'London',
    'model': '3750',
    'vendor': 'Cisco'
}, {
    'hostname': 'sw2',
    'location': 'Liverpool',
    'model': '3850',
    'vendor': 'Cisco'
}, {
    'hostname': 'sw3',
    'location': 'Liverpool',
    'model': '3650',
    'vendor': 'Cisco'
}, {
    'hostname': 'sw4',
    'location': 'London',
    'model': '3650',
    'vendor': 'Cisco'
}]


def csv_dictwriter():
    with open('csv_write_dictwriter.csv', 'w', newline='') as f:
        writer = csv.DictWriter(
            f, fieldnames=list(data[0].keys()), quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        for d in data:
            writer.writerow(d)


# --- Loads and dumps in JSON ---
# json.load - метод считывает файл в формате JSON и возвращает объекты Python.
# json.loads - метод считывает строку в формате JSON и возвращает объекты Python.

# json.dump - метод записывает объект Python в файл в формате JSON
# json.dumps - метод возвращает строку в формате JSON

trunk_template = [
    'switchport trunk encapsulation dot1q', 'switchport mode trunk',
    'switchport trunk native vlan 999', 'switchport trunk allowed vlan'
]

access_template = [
    'switchport mode access', 'switchport access vlan',
    'switchport nonegotiate', 'spanning-tree portfast',
    'spanning-tree bpduguard enable'
]

to_json = {'trunk': trunk_template, 'access': access_template}
with open('sw_templates.json', 'w') as f:
    f.write(json.dumps(to_json))
    # is equal to
    # json.dump(to_json, f)
with open('sw_templates.json') as f:
    print(f.read())

# to make data more readable
with open('sw_templates_readable.json', 'w') as f:
    json.dump(to_json, f, sort_keys=True, indent=2)
with open('sw_templates.json') as f:
    print(f.read())


class ToDo:
    def __init__(self):
        self.response = None
        self.todos = None
        # Соотношение userId с числом выполненных пользователем задач.
        self.todos_by_user = {}
        self.top_users = None
        self.max_complete = None
        self.users = []

    def create_todos(self, link):
        self.response = requests.get(link)
        self.todos = json.loads(self.response.text)

    def print_todos_info(self):
        print(self.todos == self.response.json())  # True
        print(type(self.todos))  # <class 'list'>
        print(self.todos[:10])  # ...

    def fill_todos_by_user(self):
        # Увеличение выполненных задач каждым пользователем.
        for todo in self.todos:
            if todo["completed"]:
                try:
                    # Увеличение количества существующих пользователей.
                    self.todos_by_user[todo["userId"]] += 1
                except KeyError:
                    # Новый пользователь, ставим кол-во 1.
                    self.todos_by_user[todo["userId"]] = 1

    def create_top_users(self):
        # Создание отсортированного списка пар (userId, num_complete).
        self.top_users = sorted(self.todos_by_user.items(), key=lambda x: x[1], reverse=True)

    def create_max_complete(self):
        # Получение максимального количества выполненных задач.
        self.max_complete = self.top_users[0][1]

    def create_users_with_max_tasks_completed(self):
        # Создание списка всех пользователей, которые выполнили максимальное количество задач.
        for user, num_complete in self.top_users:
            if num_complete < self.max_complete:
                break
            self.users.append(user)

    def print_users_with_max_tasks_completed(self):
        users = list(map(str, self.users))
        max_users = " and ".join(users)
        s = "s" if len(users) > 1 else ""
        print(f"user{s} {max_users} completed {self.max_complete} TODOs")

    def launch(self, link):
        self.create_todos(link)
        self.print_todos_info()
        self.fill_todos_by_user()
        self.create_top_users()
        self.create_max_complete()
        self.create_users_with_max_tasks_completed()
        self.print_users_with_max_tasks_completed()
        self.write_filtered_in_file()

    def filter_max_completed_tasks(self, todo):
        # Определить функцию для фильтра выполненных задач
        # с пользователями с максимально выполненными задачами.
        is_complete = todo["completed"]
        has_max_count = todo["userId"] in self.users
        return is_complete and has_max_count

    def write_filtered_in_file(self):
        # Записать отфильтрованные задачи в файл
        with open("filtered_data_file.json", "w") as data_file:
            filtered_todos = list(filter(self.filter_max_completed_tasks, self.todos))
            print(filtered_todos)
            json.dump(filtered_todos, data_file, indent=2)


# --- Serialization ---
z = 3 + 8j
print(type(z))  # <class 'complex'>

try:
    json.dumps(z)
except TypeError:
    "Object of type 'complex' is not JSON serializable"

print(z.real)  # 3.0
print(z.imag)  # 8.0
print(complex(3, 8) == z)  # True


def encode_complex(z):
    """ Функцию кодирования для метода dump().
    Модуль json вызовет эту функцию для любых объектов, которые не являются естественно сериализируемыми. """
    if isinstance(z, complex):
        return (z.real, z.imag)
    else:
        type_name = z.__class__.__name__
        raise TypeError(f"Object of type '{type_name}' is not JSON serializable")


json.dumps(9 + 5j, default=encode_complex)  # '[9.0, 5.0]'


# Еще один частый подход — создать дочерний класс JSONEncoder и переопределить его метод default():
class ComplexEncoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(z, complex):
            return (z.real, z.imag)
        else:
            super().default(self, z)


# Вместо создания ошибки TypeError, вы можете дать классу base справиться с ней.
# Вы можете использовать его как напрямую в метод dump() при помощи параметра cls,
# или создав экземпляр encoder-а и вызова метода encode():
complex_json = json.dumps(2 + 5j, cls=ComplexEncoder)  # '[2.0, 5.0]'
encoder = ComplexEncoder()
encoder.encode(3 + 6j)  # '[3.0, 6.0]'

json.loads(complex_json)  # [4.0, 17.0]


def decode_complex(dct):
    if "__complex__" in dct:
        return complex(dct["real"], dct["imag"])
    return dct


complex_data = {
    "__complex__": True,
    "real": 42,
    "imag": 36}

complex_data_json = json.dumps(complex_data)
print(complex_data_json)  # {"__complex__": true, "real": 42, "imag": 36}
z = json.loads(complex_data_json, object_hook=decode_complex)
print(z)  # (42+36j)

with open("complex_data.json", "w") as file:
    json.dump(complex_data, file, indent=2)

with open("complex_data.json") as complex_data:
    data = complex_data.read()  # '{\n    "__complex__": true,\n    "real": 42,\n    "imag": 36\n}'
    z = json.loads(data, object_hook=decode_complex)
    print(z)
    print(type(z))  # <class 'complex'>
# is the same as
with open("complex_data.json") as complex_data:
    z = json.load(complex_data, object_hook=decode_complex)
    print(z)
    print(type(z))  # <class 'complex'>


if __name__ == '__main__':
    todos_link = "https://jsonplaceholder.typicode.com/todos"
    todo_example = ToDo()
    # todo_example.launch(todos_link)
