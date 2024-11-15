import os
import tempfile
from models.database import database
from models.table import table
from models.field import field
from databaseManager import databaseManager


def run_test(test_func, test_name):
    try:
        test_func()
        print(f"{test_name}: PASSED")
    except AssertionError as e:
        print(f"{test_name}: FAILED -> {str(e)}")


def test_char():
    databaseManager.addDatabase("new DB")
    db = databaseManager.databases[0]
    fields = []
    fields.append(field("char", "Char"))
    t1 = table("t1", fields)
    rows = [{"char": "name"}]
    res = t1.updateRows(rows)
    assert res is False, "Тест на тип Char не пройшов"


def test_real_interval():
    databaseManager.addDatabase("new DB")
    db = databaseManager.databases[0]
    fields = []
    fields.append(field("RI", "RealInterval"))
    t1 = table("t1", fields)
    rows = [{"RI": "1.5,3.2"}]
    res = t1.updateRows(rows)
    assert res is True, "Тест на RealInterval з правильними даними не пройшов"


def test_real_interval_bad_data():
    databaseManager.addDatabase("new DB")
    db = databaseManager.databases[0]
    fields = []
    fields.append(field("RI", "RealInterval"))
    t1 = table("t2", fields)
    rows = [{"RI": "3.2,1.5"}]  # Некоректний інтервал
    res = t1.updateRows(rows)
    assert res is False, "Тест на RealInterval з некоректними даними не пройшов"


def test_picture():
    databaseManager.addDatabase("new DB")
    db = databaseManager.databases[0]
    fields = []
    fields.append(field("PictureField", "Picture"))
    t1 = table("t3", fields)

    # Створення тимчасового файлу зображення
    with tempfile.NamedTemporaryFile(suffix=".jpg") as temp_image:
        rows = [{"PictureField": temp_image.name}]
        res = t1.updateRows(rows)
        assert res is True, "Тест на тип Picture з коректними даними не пройшов"


def test_picture_bad_data():
    databaseManager.addDatabase("new DB")
    db = databaseManager.databases[0]
    fields = []
    fields.append(field("PictureField", "Picture"))
    t1 = table("t4", fields)

    # Створення тимчасового текстового файлу (не зображення)
    with tempfile.NamedTemporaryFile(suffix=".txt") as temp_non_image:
        rows = [{"PictureField": temp_non_image.name}]
        res = t1.updateRows(rows)
        assert res is False, "Тест на тип Picture з некоректними даними не пройшов"


def test_cartesian_product():
    # Створюємо базу даних і таблиці
    db = database("TestDB")
    t1 = table("Table_1", [field("A", "Int"), field("B", "Int")])
    t1.rows = [{"A": 1, "B": 1}, {"A": 2, "B": 2}]

    t2 = table("Table_2", [field("C", "Int"), field("D", "Int")])
    t2.rows = [{"C": 3, "D": 3}, {"C": 4, "D": 4}]

    db.addTable(t1)
    db.addTable(t2)

    # Виконуємо прямий добуток таблиць
    result_table = db.cartesian_product([t1, t2])

    # Очікуваний результат
    expected_rows = [
        {"A": 1, "B": 1, "C": 3, "D": 3},
        {"A": 1, "B": 1, "C": 4, "D": 4},
        {"A": 2, "B": 2, "C": 3, "D": 3},
        {"A": 2, "B": 2, "C": 4, "D": 4}
    ]

    assert result_table.rows == expected_rows, "Тест на прямий добуток таблиць не пройшов"


# Виконання тестів
run_test(test_char, "Тест для типу Char")
run_test(test_real_interval, "Тест для RealInterval (правильні дані)")
run_test(test_real_interval_bad_data, "Тест для RealInterval (некоректні дані)")
run_test(test_picture, "Тест для типу Picture (коректні дані)")
run_test(test_picture_bad_data, "Тест для типу Picture (некоректні дані)")
run_test(test_cartesian_product, "Тест для прямого добутку таблиць")
