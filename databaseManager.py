import pickle
import sys, os
#sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), './models/'))

from models.database import database
from models.table import table as appTable, table
from models.field import field
import pickle
from Pyro5.api import expose


@expose
class databaseManager():
    
    databases = []

    @staticmethod
    def getDatabases():
        return databaseManager.databases
    def getDatabase(id):
        for x in databaseManager.databases:
            if x.id == id:
                return x
    @staticmethod
    def addDatabase(name):
        d = database(name)
        databaseManager.databases.append(d)
        return d
    @staticmethod
    def deleteDatabase(id):
        for i, db in enumerate(databaseManager.databases):
            if(db.id == id):
                databaseManager.databases.remove(db)
                try:
                    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
                    rel_path = "files\\" + db.id
                    abs_file_path = os.path.join(script_dir, rel_path)
                    os.remove(abs_file_path)
                except:
                    print("Файл бази даних не знайдено в сховищі для видалення!")
                return 
    @staticmethod
    def open(name):
        db = databaseManager.getDatabase(name) 
        if (databaseManager.getDatabase(name) == None):
            script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
            rel_path = "files\\"+name
            abs_file_path = os.path.join(script_dir, rel_path)
            with open( abs_file_path , 'rb') as inp:
                db = pickle.load(inp)
            databaseManager.databases.append(db)
            return db
        return db
        
    @staticmethod
    def save(name):
        databaseManager.getDatabase(name).save(name)
    @staticmethod
    def getTables(db):
        print(db)
        db = databaseManager.getDatabase(db)
        return db.getTables()
    @staticmethod
    def getTable(db,tb):
        db = databaseManager.getDatabase(db)
        table =  db.getTable(tb)
        print('got:')
        print(table)
        return table
    @staticmethod
    def postTable(db,tb):
        print(tb)
        db = databaseManager.getDatabase(db)
        tb.__class__ = appTable
        print("aaaaa")
        fields = tb.fields.copy()
        tb.rows = []
        tb.fields = []
        for f in fields:
            newf = field(f['name'], f['type'])
            tb.fields.append(newf)
        db.addTable(tb)
        return tb
    @staticmethod
    def deleteTable(db,tb):
        db = databaseManager.getDatabase(db)
        db.deleteTable(tb)
        return 'table deleted'

    @staticmethod
    def cartesianProductTables(db, tb1, tb2):
        db = databaseManager.getDatabase(db)
        table1 = db.getTable(tb1)
        table2 = db.getTable(tb2)

        if not table1 or not table2:
            return "One or both tables not found"

        # Виконуємо прямий добуток
        result_table = db.cartesian_product([table1, table2])
        return result_table
    
    @staticmethod
    def updateRows(db,tb,rows):
        print(db, tb, rows)
        db = databaseManager.getDatabase(db)
        tb = db.getTable(tb)
        tb.updateRows(rows)
        return "rows updated"

