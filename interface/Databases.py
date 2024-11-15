
import os
import time
from tkinter import *
from tkinter import filedialog as fd
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../models/'))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))
from databaseManager import databaseManager
from CreateDatabase import CreateDatabase
from Tables import Tables
import copy


class Databases:
    def __init__(self,parent):
        self.parent = parent
        self.initUI()
    def open(self):
        filename = os.path.basename(fd.askopenfilename())
        databaseManager.open(filename)
        self.updateDb()
    
    def addDb(self,name):
        databaseManager.addDatabase(name)
        self.updateDb()

    def save(self, db):
        db.save(db.name)
        self.updateDb()

    def showCreate(self):
        window = CreateDatabase(self.parent, action = self.addDb)

    def delete(self,id):
        databaseManager.deleteDatabase(id)
        self.updateDb()

    def view(self,db):
        window = Tables(self.parent, database = db)
        
    def initUI(self):
        frame_header = Frame(self.parent, pady=2, borderwidth=2)
        frame_header.grid(column=0,row=0)

        frame_body = Frame(self.parent, pady=2, borderwidth=2, bg='grey')
        frame_body.grid(column=0,row=1, sticky="W")

        menu = Frame(frame_body, bg='green', borderwidth=2)
        menu.grid(column=0,row=1, sticky="W")

        Button(
             menu,
             text='Add db file',
             command=self.open,
             anchor='w'
         ).grid(column=1, row=0)
        Button(
            menu,
            text='Create db',
            command=self.showCreate,
            anchor='w'
        ).grid(column=2, row=0)

        self.list = Frame(frame_body, bg="green")
        self.list.grid(column=0, row=3)
        self.updateDb()

    def updateDb(self):
        databases = databaseManager.databases
        for widget in self.list.winfo_children():
            widget.destroy()
        for i, db in enumerate(databases):
            frame = Frame(self.list, borderwidth=2, pady=2, padx=2, bg="white")
            Label(frame, text=db.name, width=60, anchor="w").grid(column=0, row=0, sticky="W")
            Button(frame, text='View', command=lambda db=db: self.view(db)).grid(column=1, row=0, sticky="W")
            #if(db.isSaved == FALSE):
            Button(frame, text='Save', command=lambda db=db: self.save(db)).grid(column=2, row=0, sticky="W")
            Button(frame, text='Delete', command=lambda i=db.id: self.delete(i)).grid(column=3, row=0, sticky="W")
            frame.grid(column=0, row=i, sticky="W")
            
        
        

