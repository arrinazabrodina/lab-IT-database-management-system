import Pyro5
from Pyro5.api import expose

@expose
class field:
    def __init__(self, name, type):
        self.name = name
        self.type = type
