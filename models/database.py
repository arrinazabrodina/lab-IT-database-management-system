import os
from models.field import field
from models.table import table
import pickle
from Pyro5.api import expose


@expose
class database:

    def __init__(self, name):
        self.tables = []
        self.isSaved = False
        self.name = name
        self.id = name
        self.file = ''
        self.TABLES_IK = 0

    def addTableFromPseudo(self, _t):
        fields = []
        field_names = set()  # Збір унікальних імен полів
        print("Початок створення таблиці з полями:", _t.fields)

        for f in _t.fields:
            name = f["name"].get()
            type = f["type"].get()
            print(f"Перевірка значення поля: Ім'я = {name}, Тип = {type}")

            if name == "" or type == "":
                print("Помилка: Ім'я або тип поля порожні.")
                return False

            # Перевірка на унікальність імені поля
            if name in field_names:
                print("Помилка: Ім'я поля не унікальне.")
                return False
            field_names.add(name)

            # Додавання поля до списку
            fields.append(field(name, type))

        # Перевірка на порожню назву таблиці
        if _t.name == '':
            print("Помилка: Назва таблиці порожня.")
            return False

        print(f"Додавання таблиці '{_t.name}' з полями:", fields)

        # Додавання таблиці, якщо всі перевірки пройдені
        self.addTable(table(_t.name, fields))
        print("Таблиця успішно додана.")
        return True

    def deleteTable(self, id):
        for i, db in enumerate(self.tables):
            if (db.id == id):
                self.tables.remove(db)
                return

    def addTable(self, table):
        self.TABLES_IK += 1
        table.id = self.TABLES_IK
        self.tables.append(table)
        return table.id

    def getTables(self):
        return self.tables

    def getTable(self, id):
        for x in self.tables:
            if str(x.id) == str(id):
                return x
        return "not found"

    def save_object(self, file):
        from pathlib import Path
        current_file = Path(__file__)
        project_root = current_file.parent.parent
        filepath = os.path.join(project_root, 'files', file)
        with open(filepath, 'wb+') as outp:  # Overwrites any existing file.
            pickle.dump(self, outp, pickle.HIGHEST_PROTOCOL)

    def save(self, name):
        self.isSaved = True
        self.file = name
        self.save_object(name)

    def cartesian_product(self, tables):
        if len(tables) != 2:
            return "Для виконання прямого добутку потрібно дві таблиці."

        t1, t2 = tables
        # Створюємо нове ім'я для таблиці
        name = t1.name + "_x_" + t2.name + "_cartesian"

        # Об'єднуємо поля обох таблиць
        fields = t1.fields + t2.fields
        result_table = table(name, fields)

        # Виконуємо прямий добуток рядків
        result_rows = []
        for row1 in t1.rows:
            for row2 in t2.rows:
                combined_row = row1.copy()  # Копіюємо перший рядок
                combined_row.update(row2)  # Додаємо дані з другого рядка
                result_rows.append(combined_row)

        result_table.rows = result_rows
        self.addTable(result_table)
        return result_table
