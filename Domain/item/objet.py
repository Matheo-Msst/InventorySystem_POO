from Domain.item.item import Item 

class Objet(Item):
    def __init__(self, nom, type, soin ):
       super().__init__(nom)
       self.type = type
       self.soin =soin

    def get_description(self):
        return f"{self.nom}, type: {self.type}, soin: {self.soin}"
            
            
