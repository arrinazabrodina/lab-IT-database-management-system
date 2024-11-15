import requests

url = "http://127.0.0.1:5000"

def print_all_tables(db_id):
    response = requests.get(url + f"/{db_id}/tables")
    tables = response.json()
    print(f"Таблиці в базі даних {db_id}:")
    for table in tables:
        print(f"ID: {table['id']}, Назва: {table['name']}")

def setup_and_cartesian_product():
    # Створюємо базу даних
    requests.post(url + "?name=1")

    # Додаємо першу таблицю
    requests.post(url + "/1/tables", json={
        "id": 0,
        "name": "Table_1",
        "fields": [
            {"name": "A", "type": "Int"},
            {"name": "B", "type": "Int"}
        ]
    })
    print("Після створення Table_1:")
    print_all_tables(1)

    # Додаємо другу таблицю
    requests.post(url + "/1/tables", json={
        "id": 0,
        "name": "Table_2",
        "fields": [
            {"name": "C", "type": "Int"},
            {"name": "D", "type": "Int"}
        ]
    })
    print("Після створення Table_2:")
    print_all_tables(1)

    # Оновлюємо рядки для першої таблиці
    requests.put(url + "/1/update/1", json=[
        {
            "A": "1",
            "B": "1"
        },
        {
            "A": "2",
            "B": "2"
        },
        {
            "A": "3",
            "B": "3"
        }
    ])

    # Оновлюємо рядки для другої таблиці
    requests.put(url + "/1/update/2", json=[
        {
            "C": "4",
            "D": "4"
        },
        {
            "C": "5",
            "D": "5"
        },
        {
            "C": "6",
            "D": "6"
        }
    ])

    # Виконуємо прямий добуток таблиць
    requests.post(url + "/1/cartesian_product/1/2")

    # Виводимо таблиці після виконання прямого добутку
    print("Після виконання прямого добутку:")
    print_all_tables(1)

    # Отримуємо результати прямого добутку (новостворена таблиця)
    print("Результат прямого добутку (ID = 3, або фактичний ID нової таблиці):")
    print(requests.get(url + "/1/tables/3").content)

setup_and_cartesian_product()
