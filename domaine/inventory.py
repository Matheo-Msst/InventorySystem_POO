from typing import List, Optional
from domaine.slot import Slot
from domaine.item import Item
from pattern.singleton import Singleton

class Inventory(metaclass=Singleton):
    """Gestion de l'inventaire avec pattern Singleton"""
    
    def __init__(self, size: int = 27):
        if not hasattr(self, 'initialized'):
            self.size = size
            self.slots: List[Slot] = [Slot() for _ in range(size)]
            self.initialized = True
    
    def add_item(self, item: Item, quantity: int = 1) -> bool:
        """
        Ajoute un item à l'inventaire
        Retourne True si tout a été ajouté, False sinon
        """
        remaining = quantity
        
        # Pour les équipements, toujours créer un nouveau slot
        if item.is_equipment():
            empty_slot = self._find_empty_slot()
            if empty_slot is not None:
                self.slots[empty_slot].add(item, 1)
                print(f"✅ {item.get_display_name()} ajouté à l'inventaire (slot {empty_slot + 1})")
                return True
            else:
                print(f"❌ Inventaire plein! Impossible d'ajouter {item.get_display_name()}")
                return False
        
        # Pour les objets stackables
        # D'abord, essayer de remplir les slots existants
        for slot in self.slots:
            if not slot.is_empty() and slot.item.name == item.name:
                remaining = slot.add(item, remaining)
                if remaining == 0:
                    print(f"✅ {item.name} x{quantity} ajouté à l'inventaire")
                    return True
        
        # Ensuite, utiliser des slots vides
        while remaining > 0:
            empty_slot_idx = self._find_empty_slot()
            if empty_slot_idx is None:
                print(f"⚠️ Inventaire plein! {remaining}/{quantity} {item.name} n'ont pas pu être ajoutés")
                return False
            
            remaining = self.slots[empty_slot_idx].add(item, remaining)
        
        print(f"✅ {item.name} x{quantity} ajouté à l'inventaire")
        return True
    
    def remove_item(self, item_name: str, quantity: int = 1) -> bool:
        """Retire un item de l'inventaire"""
        remaining = quantity
        
        for slot in self.slots:
            if not slot.is_empty() and slot.item.name == item_name:
                removed = slot.remove(remaining)
                remaining -= removed
                if remaining == 0:
                    print(f"✅ {item_name} x{quantity} retiré de l'inventaire")
                    return True
        
        if remaining < quantity:
            print(f"⚠️ Seulement {quantity - remaining}/{quantity} {item_name} ont pu être retirés")
            return False
        
        print(f"❌ {item_name} non trouvé dans l'inventaire")
        return False
    
    def get_item(self, slot_index: int) -> Optional[Item]:
        """Récupère l'item d'un slot spécifique"""
        if 0 <= slot_index < self.size:
            return self.slots[slot_index].item
        return None
    
    def _find_empty_slot(self) -> Optional[int]:
        """Trouve le premier slot vide"""
        for i, slot in enumerate(self.slots):
            if slot.is_empty():
                return i
        return None
    
    def display(self):
        """Affiche l'inventaire"""
        print("\n" + "="*60)
        print("📦 INVENTAIRE".center(60))
        print("="*60)
        
        for i, slot in enumerate(self.slots):
            if not slot.is_empty():
                print(f"  [{i+1:2d}] {slot}")
        
        empty_count = sum(1 for slot in self.slots if slot.is_empty())
        print(f"\n  Slots vides: {empty_count}/{self.size}")
        print("="*60)
    
    def clear(self):
        """Vide l'inventaire (utile pour les tests)"""
        self.slots = [Slot() for _ in range(self.size)]
        print("🗑️ Inventaire vidé")
    
    def count_item(self, item_name: str) -> int:
        """Compte le nombre total d'un item dans l'inventaire"""
        total = 0
        for slot in self.slots:
            if not slot.is_empty() and slot.item.name == item_name:
                total += slot.quantity
        return total