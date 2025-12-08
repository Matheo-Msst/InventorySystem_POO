from Domain.armes import Arme
from Domain.armures import Armure

class Equipement:
    def __init__(self, nom: str):
        self.nom = nom
    def __str__(self):
        return f"Équipement: {self.nom}, Rareté: {self.rarete}"