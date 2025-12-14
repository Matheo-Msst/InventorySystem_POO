from .enchantement_pattern import WeaponEnchantementDecorator

class FireEnchantement(WeaponEnchantementDecorator):
    def __init__(self, weapon):
        super().__init__(weapon)
        self._weapon = weapon
        self.enchant_name = "Feu"
        self.enchant_power = 5
