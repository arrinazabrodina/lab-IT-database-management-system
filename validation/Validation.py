from tkinter import *
import os

class Validate:
    @staticmethod
    def String(value):
        return True

    @staticmethod
    def Real(value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    @staticmethod
    def Int(value):
        if isinstance(value, int) or (isinstance(value, str) and value.isnumeric()):
            return True
        return False

    @staticmethod
    def Char(value):
        if len(value) == 1:
            return True
        return False

    @staticmethod
    def RealInterval(value):
        values = value.split(',')
        if len(values) != 2:
            return False
        if not (Validate.Real(values[0]) and Validate.Real(values[1])):
            return False
        if float(values[0]) > float(values[1]):
            return False
        return True

    @staticmethod
    def Picture(value):
        """Перевіряє, чи є файл зображенням у форматі JPG, JPEG, PNG або GIF."""
        if os.path.isfile(value):
            extension = os.path.splitext(value)[1].lower()
            if extension in ['.jpg', '.jpeg', '.png', '.gif']:
                return True
        return False

    types = ['Int', 'String', 'Char', 'Real', 'RealInterval', 'Picture']

    def Validate(self, values, lastvalue=None, widget=None):
        res = False
        if self.type == Validate.types[0]:
            res = Validate.Int(values)
        elif self.type == Validate.types[1]:
            res = Validate.String(values)
        elif self.type == Validate.types[2]:
            res = Validate.Char(values)
        elif self.type == Validate.types[3]:
            res = Validate.Real(values)
        elif self.type == Validate.types[4]:
            res = Validate.RealInterval(values)
        elif self.type == Validate.types[5]:
            res = Validate.Picture(values)

        print(f"Перевірка значення '{values}' для поля з типом '{self.type}': {res}")

        if res is False and self.win is not None:
            entry = self.win.nametowidget(widget)
            entry.delete(0, END)

        return res if isinstance(res, bool) else False

    def __init__(self, type, win=None):
        self.type = type
        self.win = win
