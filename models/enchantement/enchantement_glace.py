from .enchantement_pattern import WeaponEnchantementDecorator
class IceEnchantement(WeaponEnchantementDecorator):
    def __init__(self, weapon):
        super().__init__(weapon)
        self._weapon = weapon
        self.enchant_name = "Glace"
        self.enchant_power = 3
