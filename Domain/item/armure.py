from Domain.item.item import Item 

class Armure(Item):
    def __init__(self, nom, point_armure, soliditer ):
       super().__init__(nom)
       self.point_armure = point_armure
       self.soliditer =soliditer

    def get_description(self):
        return f"{self.nom}, point d'armure: {self.point_armure}, soliditer: {self.soliditer}"
            
            
