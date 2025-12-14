from models.item import Item
from models.item_types.rareter import Rareter


class Weapon(Item):
    """Classe représentant une arme avec une rareté associée"""
    
    def __init__(self, id: int, name: str, rarity: Rareter, user=None, col=None):
        """
        Initialise une arme
        
        Args:
            id: Identifiant unique de l'arme
            name: Nom de l'arme
            rarity: Énumération Rareter (COMMUN, RARE, EPIC)
            user: Utilisateur propriétaire (optionnel)
            col: Colonne d'inventaire (optionnel)
        """
        super().__init__(id, name, user, col)
        self.rarity = rarity
        self.enchantements = []
    
    def get_rarity_name(self) -> str:
        """Retourne le nom lisible de la rareté"""
        return self.rarity.rareter_display_name()
    
    def get_rarity_color(self) -> str:
        """Retourne la couleur associée à la rareté"""
        return self.rarity.rareter_couleur()
    
    def __repr__(self):
        return f"Weapon(id={self.id}, name='{self.name}', rarity={self.rarity.name})"
