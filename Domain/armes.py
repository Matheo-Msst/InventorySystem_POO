class Arme :
    def __init__(self, nom: str, degats: int, portee: int, rarete: str):
        self.nom = nom
        self.rarete = rarete
        self.degats = degats
        self.portee = portee

    def __str__(self):
        return f"{self.nom}, Rareté: {self.rarete}, Dégâts: {self.degats}, Portée: {self.portee}"