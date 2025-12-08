from item import Item

class enchantement_decorateur(Item):
    """ Classe décorateur pour ajouter des enchantements à un objet existant """
    def __init__(self,item):
        self.item = item

    def get_description(self):
        """ Retourne la description de l'objet décoré """
        return self.item.get_description()
    
    def get_power(self):
        """ Retourne la puissance de l'objet décoré """
        return self.item.get_power()

