from models.item_types.armes import Weapon

class WeaponEnchantementDecorator(Weapon):
    """Classe de base pour les enchantements d'armes"""
    def __init__(self, weapon: Weapon):
        self._weapon = weapon  # l'arme originale

    def __getattr__(self, name):
        """Redirige tous les appels d'attribut vers l'arme originale si non défini ici"""
        return getattr(self._weapon, name)

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self._weapon)})"
