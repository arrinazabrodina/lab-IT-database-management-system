
import os
import time
from tkinter import *
from tkinter import filedialog as fd
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../validation/'))
from models.table import table
from Validation import Validate
from tkinter import messagebox
import copy

class CreateTable:
    def __init__(self,parent,action):
        self.parent = parent
        self.addTable = action
        self.name = StringVar()
        self.fields = []
        self.initUI()
        self.increment = 0
        self.addField()

    def action(self):
        t = table(self.name.get(), self.fields)
        res = self.addTable(t)

        if (res == True):
            self.win.destroy()


    def addField(self):
        f = {'name': StringVar(), 'type': StringVar(), "Id" : self.increment}
        self.increment = self.increment + 1
        self.fields.append(f)
        self.updateFields()

    def deleteField(self, index):
        self.fields.pop(index)
        self.updateFields()

    def initUI(self):
        self.win =  Toplevel(self.parent)
        self.win.title("Create table")
        nameFrame = Frame(self.win)
        Label(nameFrame,text ="Name").grid(row=0, column=0, sticky=W, padx=5, pady=(10, 2))
        Entry(nameFrame, textvariable = self.name).grid(row=0, column=1, sticky=W, padx=5, pady=(10, 2))
        nameFrame.grid(row=0, column = 0,  sticky=W, padx=5, pady=(10, 2))
        Label(self.win, text ="Attributes:").grid(row=1, column=0, sticky=W, padx=5, pady=(10, 2))
        self.fields_frame = Frame(self.win)
        self.fields_frame.grid(row=2, column=0)
        Button(self.win, text="Add field", command=self.addField).grid(row=3, column=0, sticky=W, padx=5, pady=(10, 2))
        Button(self.win, text="Submit", command=self.action).grid(row=10, column=0, sticky=W, padx=5, pady=(10, 2))

    def updateFields(self):
        for widget in self.fields_frame.winfo_children():
            widget.destroy()

        for i, f in enumerate(self.fields):
            frame = Frame(self.fields_frame, borderwidth=2, pady=2, padx=2, bg="white")
            Label(frame, text = 'Name').grid(row=0, column=0, sticky=W, padx=5, pady=(10, 2))
            Entry(frame, textvariable = self.fields[i]['name']).grid(row=0, column=1, sticky=W, padx=5, pady=(10, 2))
            Label(frame, text = 'Type').grid(row=0, column=2, sticky=W, padx=5, pady=(10, 2))
            OptionMenu( frame, self.fields[i]['type'], *Validate.types).grid(row=0, column=3, sticky=W, padx=5, pady=(10, 2))
            Button(frame, text = 'Delete', command=lambda index = i: self.deleteField(index)).grid(row=0, column=4, sticky=W, padx=5, pady=(10, 2))
            frame.grid(column=0, row=i, sticky="W")