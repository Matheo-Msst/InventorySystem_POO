from enum import Enum

class Rareter(Enum):
    COMMUN = 1
    RARE = 2
    EPIC = 3

    def chance_drop(self):
        """ Chance d'obtenir un des items"""
        chances = {
            self.COMMUN: 0.80,
            self.RARE: 0.15,
            self.EPIC:0.5
        }
        return chances[self]

    def rareter_couleur(self):
        """ Coueleurs associer a la rareter de l'objet"""
        couleurs = {
            self.COMMUN("white"),
            self.RARE("Vert"),
            self.EPIC("Jaune")
        }
        return couleurs[self]
