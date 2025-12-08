from enum import Enum

class Rareter(Enum):
    COMMUN = 1
    RARE = 2
    EPIC = 3

    def chance_drop(self):
        """ Chance d'obtenir un des items """
        chances = {
            Rareter.COMMUN: 0.80,
            Rareter.RARE: 0.15,
            Rareter.EPIC:0.5
        }
        return chances[self]

    def rareter_couleur(self):
        """ Couleurs associer a la rareter de l'objet """
        couleurs = {
            Rareter.COMMUN: "Blanc",
            Rareter.RARE: "Vert",
            Rareter.EPIC: "Jaune"
        }
        return couleurs[self]
