from Domain.equipement import Equipement

class Arme(Equipement):
    def __init__(self, nom: str, degats: int, portee: int, rarete: str):
        super().__init__(nom, rarete)
        self.degats = degats
        self.portee = portee

    @property
    def type_equipement(self) -> str:
        return "arme"

    def __str__(self):
        return (f"Arme: {self.nom}, Rareté: {self.rarete}, "
                f"Dégâts: {self.degats}, Portée: {self.portee}")
