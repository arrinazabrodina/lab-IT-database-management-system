from tkinter import *
from tkinter import filedialog as fd, messagebox
from PIL import Image, ImageTk  # Додано для роботи з зображеннями
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../models/'))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../validation/'))
from CreateTable import CreateTable
from Validation import Validate


class Rows:
    def __init__(self, parent, table):
        self.parent = parent
        self.table = table
        self.rows = []
        for i, r in enumerate(self.table.rows):
            row = {}
            for j, f in enumerate(self.table.fields):
                key = f.name
                val = StringVar()
                val.set(r.get(f.name, ""))  # Get the value if it exists, otherwise set an empty string
                value = {'value': val, 'type': f.type, 'thumbnail': None}  # Додаємо поле для мініатюри
                if f.type == "Picture" and val.get():  # Якщо зображення вже вибране, завантажуємо мініатюру
                    value['thumbnail'] = self.create_thumbnail(val.get())
                row[key] = value
            self.rows.append(row)
        self.initUI()

    def addRow(self):
        row = {}
        for j, f in enumerate(self.table.fields):
            val = StringVar()
            row[f.name] = {'value': val, 'type': f.type, 'thumbnail': None}
        self.rows.append(row)
        self.updateRows()

    def deleteRow(self, i):
        self.rows.pop(i)
        self.updateRows()

    def save(self):
        rows = []
        for i, r in enumerate(self.rows):
            row_dict = {}
            for j, f in enumerate(self.table.fields):
                val = r[f.name]['value'].get()
                row_dict[f.name] = val
            rows.append(row_dict)
        res = self.table.updateRows(rows)
        if not res:
            messagebox.showerror('Error', 'Some of the values are invalid')

    def initUI(self):
        window = Toplevel(self.parent, pady=2, borderwidth=2)
        window.title("Table rows")
        frame_header = Frame(window, pady=2, borderwidth=2)
        frame_header.grid(column=0, row=0)

        frame_body = Frame(window, pady=2, borderwidth=2, bg='grey')
        frame_body.grid(column=0, row=1, sticky="W")

        menu = Frame(frame_body, bg='green', borderwidth=2)
        menu.grid(column=0, row=1, sticky="W")

        self.list = Frame(frame_body)
        self.list.grid(column=0, row=3, sticky="W")

        Button(
            menu,
            text='Add row',
            command=self.addRow,
            anchor='w'
        ).grid(column=0, row=4, sticky="W", pady=2)
        Button(
            frame_body,
            text='Apply changes',
            command=self.save,
            anchor='w'
        ).grid(column=0, row=5, sticky="W", pady=2)

        self.updateRows()

    def updateRows(self):
        for widget in self.list.winfo_children():
            widget.destroy()

        for i, f in enumerate(self.table.fields):
            label = Label(self.list, text=f.name)
            label.grid(row=0, column=i, sticky=NSEW)

        for i, r in enumerate(self.rows):
            for j, f in enumerate(self.table.fields):
                if f.type == "Picture":
                    # Створення кнопки для вибору файлу зображення
                    Button(self.list, text="Завантажити зображення",
                           command=lambda r=r, f=f: self.load_picture(r, f.name, i, j)).grid(row=i + 1, column=j)

                    # Відображення мініатюри, якщо вона існує
                    if r[f.name]['thumbnail']:
                        label = Label(self.list, image=r[f.name]['thumbnail'])
                        label.image = r[f.name]['thumbnail']  # Зберігаємо посилання, щоб уникнути видалення зображення
                        label.grid(row=i + 1, column=j + 1)
                else:
                    # Створення звичайного текстового поля для інших типів
                    v = Validate(f.type, self.list)
                    vcmd = self.parent.register(v.Validate)
                    input_field = Entry(self.list, textvariable=r[f.name]['value'], validate='focusout',
                                        validatecommand=(vcmd, '%P', '%s', '%W'))
                    input_field.grid(row=i + 1, column=j)
            Button(self.list, text='Delete', command=lambda i=i: self.deleteRow(i)).grid(row=i + 1, column=j + 2,
                                                                                         sticky=NSEW)

    def load_picture(self, row, field_name, row_index, col_index):
        # Відкриття діалогового вікна для вибору файлу
        file_path = fd.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif")])
        if file_path:
            # Збереження обраного шляху до файлу у відповідному полі
            row[field_name]['value'].set(file_path)
            row[field_name]['thumbnail'] = self.create_thumbnail(file_path)  # Створення та збереження мініатюри
            self.updateRows()  # Оновлення відображення рядків

    def create_thumbnail(self, file_path):
        # Завантаження зображення і створення мініатюри
        img = Image.open(file_path)
        img.thumbnail((50, 50))  # Розмір мініатюри
        return ImageTk.PhotoImage(img)
