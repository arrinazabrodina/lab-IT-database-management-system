import os
from tkinter import *
from tkinter import filedialog as fd, messagebox
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../models/'))
from CreateTable import CreateTable
from Rows import Rows
from database import database


class Tables:
    def __init__(self, parent, database):
        self.parent = parent
        self.db = database
        self.initUI()

    def showCreate(self):
        window = CreateTable(self.parent, action=self.addTable)

    def addTable(self, pseudo_table):
        res = self.db.addTableFromPseudo(pseudo_table)
        if res == False:
            messagebox.showerror('Error', 'Some of the values are invalid')
            return False
        else:
            self.updateTables()
            return True

    def delete(self, id):
        self.db.deleteTable(id)
        self.updateTables()

    def view(self, table):
        window = Rows(self.parent, table)

    def initUI(self):
        window = Toplevel(self.parent, pady=2, borderwidth=2)
        window.title("Database tables")
        frame_header = Frame(window, pady=2, borderwidth=2)
        frame_header.grid(column=0, row=0)

        frame_body = Frame(window, pady=2, borderwidth=2, bg='grey')
        frame_body.grid(column=0, row=1, sticky="W")

        menu = Frame(frame_body, bg='green', borderwidth=2)
        menu.grid(column=0, row=1, sticky="W")

        Button(
            menu,
            text='Create table',
            command=self.showCreate,
            anchor='w'
        ).grid(column=0, row=0, sticky="W")
        Button(
            menu,
            text='Cartesian Product',
            command=self.show_cartesian_product_window,
            anchor='w'
        ).grid(column=1, row=0, sticky="W")

        self.list = Frame(frame_body)
        self.list.grid(column=0, row=3)
        self.updateTables()

    def show_cartesian_product_window(self):
        # Відкриття нового вікна для вибору таблиць
        self.cartesian_window = Toplevel(self.parent)
        self.cartesian_window.title("Select Tables for Cartesian Product")

        Label(self.cartesian_window, text="Select two tables for Cartesian Product:").grid(row=0, column=0,
                                                                                           columnspan=2, padx=10,
                                                                                           pady=10)

        self.selected_tables = []  # Список для збереження вибраних таблиць

        tables = self.db.getTables()
        for i, table in enumerate(tables):
            var = IntVar()
            chk = Checkbutton(self.cartesian_window, text=table.name, variable=var,
                              command=lambda t=table, v=var: self.toggle_selection(t, v))
            chk.grid(row=i + 1, column=0, sticky="w", padx=10)

        Button(self.cartesian_window, text="Calculate Product", command=self.calculate_cartesian_product).grid(
            row=len(tables) + 1, column=0, padx=10, pady=10)

    def toggle_selection(self, table, var):
        # Додавання або видалення таблиці зі списку вибраних
        if var.get() == 1:
            if len(self.selected_tables) < 2:
                self.selected_tables.append(table)
            else:
                messagebox.showwarning("Selection Limit", "You can select only two tables.")
                var.set(0)
        else:
            if table in self.selected_tables:
                self.selected_tables.remove(table)

    def calculate_cartesian_product(self):
        # Перевірка, що вибрано рівно дві таблиці
        if len(self.selected_tables) != 2:
            messagebox.showerror("Error", "Please select exactly two tables.")
            return

        result_table = self.db.cartesian_product(self.selected_tables)
        if isinstance(result_table, str):
            messagebox.showerror('Error', result_table)
        else:
            messagebox.showinfo('Success', f'Cartesian product table "{result_table.name}" created.')
            self.updateTables()
            self.cartesian_window.destroy()  # Закриття вікна після успішної операції

    def updateTables(self):
        tables = self.db.getTables()
        for widget in self.list.winfo_children():
            widget.destroy()
        for i, t in enumerate(tables):
            frame = Frame(self.list, borderwidth=2, pady=2, padx=2, bg="white")
            frame.table = t
            Label(frame, text=t.name, width=60, anchor="w").grid(column=0, row=0, sticky="W")
            Button(frame, text='View', command=lambda t=t: self.view(t)).grid(column=1, row=0, sticky="W")
            Button(frame, text='Delete', command=lambda i=t.id: self.delete(i)).grid(column=2, row=0, sticky="W")
            frame.grid(column=0, row=i, sticky="W")
