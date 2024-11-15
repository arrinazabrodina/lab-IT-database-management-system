
from tkinter import *
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'interface'))

from Databases import Databases
root = Tk()
root.title("My Databases")
root.resizable(False, False)

# Execute Tkinter
p = Databases(root)
root.mainloop()