from .equipement import Equipement

class Armure(Equipement):
    def __init__(self, nom: str, defense: int, rarete: str):
        super().__init__(nom, rarete)
        self.defense = defense

    @property
    def type_equipement(self) -> str:
        return "armure"

    def __str__(self):
        return (f"Armure: {self.nom}, Rareté: {self.rarete}, "
                f"Défense: {self.defense}")
