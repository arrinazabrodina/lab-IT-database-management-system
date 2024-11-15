
import os
import time
from tkinter import *
from tkinter import filedialog as fd
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../models/'))

class CreateDatabase:
    def __init__(self,parent,action):
        self.parent = parent
        self.addDb = action
        self.name = StringVar()
        self.initUI()

    def action(self):
        self.win.destroy()
        self.addDb(self.name.get())
        
        
    def initUI(self):
        self.win =  Toplevel(self.parent)
        self.parent.eval(f'tk::PlaceWindow {str(self.win)} center')
        Label(self.win,
            text ="Name").grid(row=0, column=0, sticky=W, padx=5, pady=(10, 2))
        Entry(self.win, textvariable = self.name).grid(row=0, column=0, sticky=W, padx=5, pady=(10, 2))
        Button(self.win, text="Submit", command=self.action).grid(row=1, column=0, sticky=W, padx=5, pady=(10, 2))