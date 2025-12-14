from enum import Enum
from models.item import Item


class RessourceType(Enum):
    """Énumération des types de ressources disponibles"""
    BOIS = {
        "name": "Bois",
        "emoji": "🪵",
        "max_stack": 64,
        "color": "#8B4513"
    }
    PIERRE = {
        "name": "Pierre",
        "emoji": "🪨",
        "max_stack": 64,
        "color": "#A9A9A9"
    }
    OR = {
        "name": "Or",
        "emoji": "✨",
        "max_stack": 32,
        "color": "#FFD700"
    }
    FER = {
        "name": "Fer",
        "emoji": "⚙️",
        "max_stack": 48,
        "color": "#C0C0C0"
    }
    DIAMANT = {
        "name": "Diamant",
        "emoji": "💎",
        "max_stack": 16,
        "color": "#00CED1"
    }
    CHARBON = {
        "name": "Charbon",
        "emoji": "🔥",
        "max_stack": 128,
        "color": "#36454F"
    }

    def get_info(self):
        """Retourne les informations du type de ressource"""
        return self.value

    def get_name(self):
        """Retourne le nom de la ressource"""
        return self.value["name"]

    def get_emoji(self):
        """Retourne l'emoji de la ressource"""
        return self.value["emoji"]

    def get_max_stack(self):
        """Retourne la quantité maximale stackable"""
        return self.value["max_stack"]

    def get_color(self):
        """Retourne la couleur de la ressource"""
        return self.value["color"]


class Resource(Item):
    """
    Classe pour les ressources stackables
    Contrairement aux armes, les ressources peuvent être empilées jusqu'à une limite
    """

    def __init__(self, id, resource_type: RessourceType, quantity: int = 1, col=None, user=None):
        """
        Initialise une ressource

        Args:
            id: Identifiant unique de la ressource
            resource_type: Type de ressource (enum RessourceType)
            quantity: Quantité de ressources (1 à max_stack)
            col: Emplacement dans l'inventaire
            user: Propriétaire de la ressource
        """
        super().__init__(id, resource_type.get_name())
        self.resource_type = resource_type
        # S'assurer que la quantité ne dépasse pas le maximum
        self.quantity = min(quantity, resource_type.get_max_stack())
        self.col = col
        self.user = user

    def add_quantity(self, amount: int) -> int:
        """
        Ajoute de la quantité à la ressource

        Args:
            amount: Quantité à ajouter

        Returns:
            Quantité restante qui n'a pu être ajoutée (débordement)
        """
        new_quantity = self.quantity + amount
        max_stack = self.resource_type.get_max_stack()

        if new_quantity <= max_stack:
            self.quantity = new_quantity
            return 0  # Rien n'a débordé
        else:
            overflow = new_quantity - max_stack
            self.quantity = max_stack
            return overflow  # Retourne le débordement

    def remove_quantity(self, amount: int) -> bool:
        """
        Retire de la quantité à la ressource

        Args:
            amount: Quantité à retirer

        Returns:
            True si la suppression a réussi, False sinon
        """
        if amount <= self.quantity:
            self.quantity -= amount
            return True
        return False

    def is_full(self) -> bool:
        """Vérifie si la ressource est remplie au maximum"""
        return self.quantity >= self.resource_type.get_max_stack()

    def get_emoji(self) -> str:
        """Retourne l'emoji de la ressource"""
        return self.resource_type.get_emoji()

    def get_max_stack(self) -> int:
        """Retourne la quantité maximale stackable"""
        return self.resource_type.get_max_stack()

    def get_color(self) -> str:
        """Retourne la couleur de la ressource"""
        return self.resource_type.get_color()

    def is_stackable_with(self, other: 'Resource') -> bool:
        """
        Vérifie si cette ressource peut être stackée avec une autre

        Args:
            other: Autre ressource

        Returns:
            True si les deux ressources sont du même type et non pleines
        """
        if not isinstance(other, Resource):
            return False
        return (
            self.resource_type == other.resource_type and
            not self.is_full()
        )

    def __repr__(self):
        return f"Resource({self.name} x{self.quantity}/{self.get_max_stack()})"
