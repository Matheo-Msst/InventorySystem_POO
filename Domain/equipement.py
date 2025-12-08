from abc import ABC, abstractmethod

class Equipement(ABC):
    def __init__(self, nom: str, rarete: str):
        self.nom = nom
        self.rarete = rarete

    @property
    @abstractmethod
    def type_equipement(self) -> str:
        """Doit retourner 'arme', 'armure', etc."""
        pass

    def __str__(self):
        return f"{self.nom} ({self.type_equipement}), Rareté: {self.rarete}"
