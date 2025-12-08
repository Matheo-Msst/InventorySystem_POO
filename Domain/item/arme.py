from item import Item 

class Weapon(Item):
    def __init__(self, nom, rareter, dommage):
       super.__init__(nom, rareter)
       self.dommage = dommage

    def get_description(self):
        return f"{self.nom} ({self.rareter})"
            
    def get_power(self):
        self.dommage
        