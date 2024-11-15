from Pyro5.api import expose
import sys
import os

# Додає кореневу папку до sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from databaseManager import databaseManager
from models.table import table as appTable
from models.field import field



@expose
class RmiDatabaseManager:

    def add_database(self, name):
        """Додає базу даних та повертає її у вигляді словника."""
        db = databaseManager.addDatabase(name)
        return self.database_to_dict(db)

    def get_databases(self):
        """Повертає список усіх баз даних у вигляді словників."""
        return [self.database_to_dict(db) for db in databaseManager.getDatabases()]

    def delete_database(self, db_id):
        """Видаляє базу даних за ідентифікатором."""
        databaseManager.deleteDatabase(db_id)
        return f"База даних '{db_id}' видалена"

    def open_database(self, name):
        """Відкриває базу даних і повертає її у вигляді словника."""
        db = databaseManager.open(name)
        return self.database_to_dict(db) if db else f"База даних '{name}' не знайдена"

    def save_database(self, name):
        """Зберігає базу даних."""
        databaseManager.save(name)
        return f"База даних '{name}' збережена"

    def get_tables(self, db_name):
        """Повертає список таблиць у базі даних у вигляді словників."""
        db = databaseManager.getDatabase(db_name)
        if db:
            return [self.table_to_dict(tbl) for tbl in db.getTables()]
        return f"База даних '{db_name}' не знайдена"

    def add_table(self, db_name, table_data):
        """Додає таблицю до бази даних."""
        db = databaseManager.getDatabase(db_name)
        if db:
            fields = [self.dict_to_field(f) for f in table_data["fields"]]
            new_table = appTable(table_data["name"], fields)
            return db.addTable(new_table)
            return f"Таблиця '{table_data['name']}' додана до бази даних '{db_name}'"
        return f"База даних '{db_name}' не знайдена"

    def delete_table(self, db_name, table_id):
        """Видаляє таблицю з бази даних."""
        db = databaseManager.getDatabase(db_name)
        if db:
            db.deleteTable(table_id)
            return f"Таблиця '{table_id}' видалена з бази даних '{db_name}'"
        return f"База даних '{db_name}' не знайдена"

    def update_rows(self, db_name, table_id, rows):
        print(f"update_rows викликаний з параметрами db_name: {db_name}, table_id: {table_id}, rows: {rows}")
        """Оновлює рядки в таблиці."""
        db = databaseManager.getDatabase(db_name)
        if db:
            tbl = db.getTable(table_id)
            if tbl:
                print(tbl.name)
                tbl.updateRows(rows)
                print(tbl.rows)
                return "Рядки оновлені"
            return f"Таблиця '{table_id}' не знайдена в базі даних '{db_name}'"
        return f"База даних '{db_name}' не знайдена"

    def intersect_tables(self, db_name, table1_id, table2_id):
        """Знаходить перетин між двома таблицями та повертає нову таблицю як словник."""
        db = databaseManager.getDatabase(db_name)
        if db:
            intersect_table = db.intersect([db.getTable(table1_id), db.getTable(table2_id)])
            return self.table_to_dict(intersect_table) if intersect_table else "Перетин неможливий"
        return f"База даних '{db_name}' не знайдена"

    # Методи для перетворення об'єктів на словники та навпаки
    def database_to_dict(self, db):
        return {
            "name": db.name,
            "tables": [self.table_to_dict(t) for t in db.getTables()],
            "isSaved": db.isSaved,
            "id": db.id,
            "file": db.file
        }

    def table_to_dict(self, tbl):
        return {
            "name": tbl.name,
            "fields": [self.field_to_dict(f) for f in tbl.fields],
            "id": tbl.id,
            "rows": tbl.rows
        }

    def field_to_dict(self, fld):
        return {
            "name": fld.name,
            "type": fld.type
        }

    def dict_to_field(self, field_data):
        """Перетворює словник у об'єкт field."""
        return field(field_data["name"], field_data["type"])
