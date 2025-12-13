from enum import Enum

class EnchantmentType(Enum):
    """Types d'enchantements disponibles"""
    SHARPNESS = ("Tranchant", "Augmente les dégâts de +5")
    PROTECTION = ("Protection", "Réduit les dégâts reçus de 10%")
    FIRE = ("Feu", "Ajoute des dégâts de feu")
    
    def __init__(self, display_name, description):
        self.display_name = display_name
        self.description = description
    
    def __str__(self):
        return f"{self.display_name}: {self.description}"


class Enchantment:
    """Représente un enchantement appliqué à un équipement"""
    
    def __init__(self, enchantment_type: EnchantmentType, level: int = 1):
        self.type = enchantment_type
        self.level = min(max(level, 1), 5)  # Niveau entre 1 et 5
    
    def __str__(self):
        return f"{self.type.display_name} {self.level}"
    
    def __repr__(self):
        return f"Enchantment({self.type.name}, level={self.level})"