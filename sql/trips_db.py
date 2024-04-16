# Код из курса "Интерактивный тренажёр SQL" https://stepik.org/course/63054/syllabus
from sqlite3 import connect
from os import getcwd as os_getcwd


class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance


class DBCommitter(Singleton):
    quotes = ['«', '»', '„', '“', "'", '"']

    def __init__(self, db_name: str):
        if not hasattr(self, 'db_name'):
            self.db_name = db_name

    def get_db_name(self):
        return self.__db_name

    def set_db_name(self, db_name):
        self.__db_name = self.db_name_check(db_name=db_name)

    db_name = property(get_db_name, set_db_name)

    def db_name_check(self, db_name: str, db_format: str = ".db"):
        if type(db_name) != str or not db_name.endswith(db_format.strip()):
            raise TypeError(f"Неверно поданное значение параметра db_name = <{db_name}>!")
        return db_name.strip()

    def table_name_check(self, table_name: str):
        # проверки на валидность названия таблицы
        # тип данных
        if type(table_name) != str:
            raise TypeError(f"Неверно поданное значение параметра table_name = <{table_name}>!")
        table_name = table_name.strip()
        # цифры в начале строки
        if (table_name[0]).isdigit():
            raise TypeError(f"Название таблицы начинается с цифры: <{table_name}>!")
        # работа с большими пробелами
        while "  " in table_name:
            table_name = table_name.replace("  ", " ")
        # удаление лишних символов за исключением лат букв, цифр и пробелов + """"""
        getVals = list([val for val in table_name
                        if val.isalpha() or val.isnumeric() or val == " " or val in self.quotes])
        table_name_refined = "".join(getVals)
        # заменяем пробелы на нижнее подчеркивание (если нету кавычек в названии!)
        if any([val in self.quotes for val in table_name_refined]):
            pass
        else:
            table_name_refined = table_name_refined.replace(" ", "_")
        if len(table_name_refined) != len(table_name):
            print(f"Исправленное название таблицы: {table_name_refined}")
            return [table_name, table_name_refined][self.is_right_answer(question_text="Принять исправление?")]
        else:
            return table_name

    def is_right_answer(self, question_text: str):
        answer = input(f"{question_text} (введите да / нет или yes / no или 1 / 0)\n")
        yes = ['yes', 'да', "1"]
        no = ['no', 'нет', "0"]
        return answer.lower().strip() in yes

    def create_db_table(self, table_name: str, colnames_data_types: dict):
        tbl_name = self.table_name_check(table_name)
        print(tbl_name)
        # устанавливаем соединение с БД
        conn = connect(self.db_name)
        # d_name_str = tbl_name
        c = conn.cursor()  # заводим курсор
        # основная структура запроса - здесь:
        colnames_info_str = ', '.join([f'{k} {v}'
                                       for (k, v) in colnames_data_types.items()])
        query = f'''CREATE TABLE IF NOT EXISTS {tbl_name}
             ({colnames_info_str})'''
        c.execute(query)
        conn.commit()  # делаем коммит
        conn.close()  # закрываем соединение
        print(f"table <{tbl_name}> has been successfully created")
        print(f"in the current directory: <{os_getcwd()}>")
        print(f"with <{len(colnames_data_types)}> columns")
        return query

    def insert_data_table(self,
                          table_name: str,
                          colnames_data_types: dict,
                          data: tuple):
        tbl_name = table_name
        # print(tbl_name)
        # осуществляем проверку на наличие таблицы с заданным названием в БД
        conn = connect(self.db_name)
        c = conn.cursor()  # заводим курсор
        sql_query = """SELECT name FROM sqlite_master WHERE type='table';"""
        c.execute(sql_query)
        db_tables = c.fetchall()
        conn.close()  # закрываем соединение
        if not any([i[0] == tbl_name for i in db_tables]):
            raise TypeError(f"БД {self.db_name} не содержит таблицы: <{tbl_name}>!")
        # print(*[i[0] for i in db_tables], sep='\n')

        # НЕПОСРЕДСТВЕННО САМА ВСТАВКА ДАННЫХ В БД (после успешного поиска имени таблицы в БД):
        # устанавливаем соединение с БД
        conn = connect(self.db_name)
        c = conn.cursor()  # заводим курсор

        # основная структура запроса - здесь:
        colnames_info_str = ', '.join([f'{k}'
                                       for (k, v) in colnames_data_types.items()
                                       if 'id' not in k])
        # print(data)
        insert_query = f'''INSERT INTO {tbl_name}
             ({colnames_info_str}) VALUES
             ({', '.join(['?' for i in range(len(data[0]))])})
             '''
        print(insert_query)
        values_to_insert = tuple(tuple([i for i in elem]) for elem in data)
        print(*values_to_insert)
        for row in values_to_insert:
            c.execute(insert_query, row)
            conn.commit()
        conn.close()  # закрываем соединение

    def delete_duplicates(self, table_name: str, colnames_data_types: dict):
        """ At the moment I didn't know how to implement a dynamic check if the record already exists
         So that each time this code is relaunched extra 20 records were added to the table.
         Here comes delete_duplicates func to get rid of all dupes
         assuming the records are equal if all non-id fields are equal"""
        tbl_name = table_name
        colnames_info_lst = [f'{k}' for (k, v) in colnames_data_types.items() if 'id' not in k]
        where_condition = ' AND '.join([f'{tbl_name}.{colname} = t.{colname}' for colname in colnames_info_lst])
        delete_query = f"""DELETE FROM {tbl_name}
                            WHERE trip_id > (
                              SELECT MIN(trip_id) FROM {tbl_name} t
                              WHERE {where_condition}
                            );"""
        with connect(self.db_name) as conn:
            c = conn.cursor()
            c.execute(delete_query)
            conn.commit()


if __name__ == '__main__':
    db_trip_data = {
        "trip_id": "INTEGER PRIMARY KEY",
        "name": "VARCHAR(30)",
        "city": "VARCHAR(25)",
        "per_diem": "DECIMAL(8, 2)",
        "date_first": "DATE",
        "date_last": "DATE"
    }
    data_insert = (
        ('Баранов П.Е.', 'Москва', 700, '2020-01-12', '2020-01-17'),
        ('Абрамова К.А.', 'Владивосток', 450, '2020-01-14', '2020-01-27'),
        ('Семенов И.В.', 'Москва', 700, '2020-01-23', '2020-01-31'),
        ('Ильиных Г.Р.', 'Владивосток', 450, '2020-01-12', '2020-02-02'),
        ('Колесов С.П.', 'Москва', 700, '2020-02-01', '2020-02-06'),
        ('Баранов П.Е.', 'Москва', 700, '2020-02-14', '2020-02-22'),
        ('Абрамова К.А.', 'Москва', 700, '2020-02-23', '2020-03-01'),
        ('Лебедев Т.К.', 'Москва', 700, '2020-03-03', '2020-03-06'),
        ('Колесов С.П.', 'Новосибирск', 450, '2020-02-27', '2020-03-12'),
        ('Семенов И.В.', 'Санкт-Петербург', 700, '2020-03-29', '2020-04-05'),
        ('Абрамова К.А.', 'Москва', 700, '2020-04-06', '2020-04-14'),
        ('Баранов П.Е.', 'Новосибирск', 450, '2020-04-18', '2020-05-04'),
        ('Лебедев Т.К.', 'Томск', 450, '2020-05-20', '2020-05-31'),
        ('Семенов И.В.', 'Санкт-Петербург', 700, '2020-06-01', '2020-06-03'),
        ('Абрамова К.А.', 'Санкт-Петербург', 700, '2020-05-28', '2020-06-04'),
        ('Федорова А.Ю.', 'Новосибирск', 450, '2020-05-25', '2020-06-04'),
        ('Колесов С.П.', 'Новосибирск', 450, '2020-06-03', '2020-06-12'),
        ('Федорова А.Ю.', 'Томск', 450, '2020-06-20', '2020-06-26'),
        ('Абрамова К.А.', 'Владивосток', 450, '2020-07-02', '2020-07-13'),
        ('Баранов П.Е.', 'Воронеж', 450, '2020-07-19', '2020-07-25')
    )

    trip_obj = DBCommitter(db_name="trip.db")
    print(trip_obj.__dict__)

    q_1 = trip_obj.create_db_table("trip", db_trip_data)
    print(q_1)

    trip_obj.insert_data_table(table_name="trip",
                               colnames_data_types=db_trip_data,
                               data=data_insert)

    trip_obj.delete_duplicates(table_name="trip",
                               colnames_data_types=db_trip_data)

    trip_obj.db_name = "trip_1.db"
    print(trip_obj, trip_obj.__dict__)
    # проверяем корректность работы паттерна "Singletone"
    trip_obj_3 = DBCommitter(db_name="trip_3.db")
    print(trip_obj_3, trip_obj_3.__dict__)
    print("^ ^ ^")
    print("| | |")
    print("Все копии объектов класса DBCommitter по факту ссылаются на один объект!")
