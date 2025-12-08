from Domain import equipement


class Armure(equipement.Equipement):
    def __init__(self, nom: str, defense: int, rarete: str):
        self.nom = nom
        self.rarete = rarete
        self.defense = defense

    def __str__(self):
        return f"Armure: {self.nom}, Rareté: {self.rarete}, Défense: {self.defense}"