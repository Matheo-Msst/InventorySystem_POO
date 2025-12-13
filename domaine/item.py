from typing import Optional, List
from domaine.rarity import Rarity
from domaine.enchantment import Enchantment

class Item:
    """Classe de base pour tous les items"""
    
    def __init__(self, name: str, image: str, max_stack: int = 64,
                 rarity: Optional[Rarity] = None):
        self.name = name
        self.image = image
        self.max_stack = max_stack
        self.rarity = rarity
        self.enchantments: List[Enchantment] = []

    def is_equipment(self) -> bool:
        return self.rarity is not None

    def add_enchantment(self, enchantment: Enchantment) -> bool:
        if not self.is_equipment():
            return False
        for enc in self.enchantments:
            if enc.type == enchantment.type:
                enc.level = min(enc.level + 1, 5)
                return True
        self.enchantments.append(enchantment)
        return True

    def get_display_name(self) -> str:
        enchant_str = f" [{', '.join(str(e) for e in self.enchantments)}]" if self.enchantments else ""
        if self.rarity:
            return f"[{self.rarity.value}] {self.name}{enchant_str}"
        return f"{self.name}{enchant_str}"

    def __str__(self):
        return self.get_display_name()

    def __repr__(self):
        return f"Item({self.name}, rarity={self.rarity})"
