from Domain.item.item import Item 

class Arme(Item):
    def __init__(self, nom, rareter, degat, porter):
       super().__init__(nom)
       self.rareter = rareter
       self.degat = degat
       self.porter = porter

    def get_description(self):
        return f"{self.nom} ({self.rareter.name}) , dégâts: {self.degat}, portée: {self.porter}"
            
