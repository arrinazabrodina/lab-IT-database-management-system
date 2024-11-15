import Pyro5.api
import os
uri_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "uri.txt")


def connect_to_server():
    with open(uri_file, "r") as file:
        uri = file.read().strip()

    return Pyro5.api.Proxy(uri)


def main():
    db_manager = connect_to_server()
    db_name = "TestDB"

    db_dict = db_manager.add_database(db_name)
    print("Створено базу даних:", db_dict)
    print("Список баз даних:", db_manager.get_databases())

    table_data = {
        "name": "Users",
        "fields": [{"name": "ID", "type": "Int"}, {"name": "Name", "type": "String"}]
    }
    id_tb = db_manager.add_table(db_name, table_data)
    print("Таблиці:", db_manager.get_tables(db_name))

    rows = [
        {"ID": "1", "Name": "Alice"},
        {"ID": "2", "Name": "Bob"}
    ]
    print(db_manager.update_rows(db_name, id_tb, rows))

    tables = db_manager.get_tables(db_name)
    print("Таблиці:", tables)

    print(db_manager.save_database(db_name))


if __name__ == "__main__":
    main()