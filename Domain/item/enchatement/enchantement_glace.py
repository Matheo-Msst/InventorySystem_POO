from enchantement import enchantement_decorateur

class Enchantement_glace(enchantement_decorateur):
    """Classe représentant un enchantement de type Glace"""
    def get_description(self):
        """Retourne la description de l'objet avec l'enchantement Glace"""
        return super().get_description() + "Glace"
    
    def get_power(self):
        """Retourne la puissance de l'objet augmentée de 10 """
        return super().get_power() + 10