from typing import Optional
from domaine.item import Item

class Slot:
    """Représente un emplacement d'inventaire pouvant contenir un certain nombre d'items identiques"""
    
    def __init__(self, item: Optional[Item] = None, quantity: int = 0):
        self.item = item
        self.quantity = quantity if item else 0
    
    def is_empty(self) -> bool:
        """Vérifie si le slot est vide"""
        return self.item is None or self.quantity == 0
    
    def can_add(self, item: Item, quantity: int = 1) -> bool:
        """Vérifie s'il est possible d'ajouter l'item"""
        if self.is_empty():
            return True
        
        # Vérifier si c'est le même item (nom identique)
        if self.item.name != item.name:
            return False
        
        # Les équipements ne peuvent pas être stackés (même nom mais enchantements différents)
        if item.is_equipment():
            return False
        
        # Vérifier le maximum de stack
        return self.quantity + quantity <= self.item.max_stack
    
    def add(self, item: Item, quantity: int = 1) -> int:
        """
        Ajoute des items au slot
        Retourne le nombre d'items qui n'ont pas pu être ajoutés
        """
        if self.is_empty():
            self.item = item
            added = min(quantity, item.max_stack)
            self.quantity = added
            return quantity - added
        
        if not self.can_add(item, quantity):
            return quantity
        
        max_can_add = self.item.max_stack - self.quantity
        added = min(quantity, max_can_add)
        self.quantity += added
        return quantity - added
    
    def remove(self, quantity: int = 1) -> int:
        """
        Retire des items du slot
        Retourne le nombre d'items effectivement retirés
        """
        if self.is_empty():
            return 0
        
        removed = min(quantity, self.quantity)
        self.quantity -= removed
        
        if self.quantity == 0:
            self.item = None
        
        return removed
    
    def __str__(self):
        if self.is_empty():
            return "[Vide]"
        return f"{self.item.get_display_name()} x{self.quantity}"
    
    def __repr__(self):
        return f"Slot(item={self.item.name if self.item else None}, qty={self.quantity})"