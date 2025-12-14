from enum import Enum

class Rareter(Enum):
    COMMUN = 1
    RARE = 2
    EPIC = 3

    def chance_drop(self):
        """Chance d'obtenir un des items"""
        chances = {
            self.COMMUN: 0.70,
            self.RARE: 0.25,
            self.EPIC: 0.05
        }
        return chances[self]

    def rareter_couleur(self):
        """Couleurs associées à la rareté de l'objet"""
        couleurs = {
            self.COMMUN: "white",
            self.RARE: "green",
            self.EPIC: "gold"
        }
        return couleurs[self]

    def rareter_display_name(self):
        """Nom lisible de la rareté"""
        noms = {
            self.COMMUN: "Commun",
            self.RARE: "Rare",
            self.EPIC: "Épique"
        }
        return noms[self]
