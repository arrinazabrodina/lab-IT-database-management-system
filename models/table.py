import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))
from validation.Validation import Validate

from Pyro5.api import expose
from .field import field

@expose
class table:
    def __init__(self, name, fields):
        self.name = name
        self.id = name
        self.fields = fields
        self.rows = []

    def validate(self, _rows):
        for (i, r) in enumerate(_rows):
            for (j, f) in enumerate(self.fields):
                val = r[f.name]
                v = Validate(f.type)
                if not v.Validate(val):
                    return False
        return True


    def updateRows(self, rows):
        if not self.validate(rows):
            return False
        self.rows = rows
        return True

