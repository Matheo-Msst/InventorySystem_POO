class Item:
    """ Classe de base pour tout objet (Item) du jeu """
    def __init__(self, nom, rareter):
       self.nom = nom
       self.rareter = rareter 

    def get_description(self):
        """ Retourne la description de l'objet """
        raise NotImplementedError
    
    def get_power(self):
        """ Retourne la puissance de l'objet """
        return 0