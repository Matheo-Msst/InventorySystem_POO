from enchantement import enchantement_decorateur

class Enchantement_feu(enchantement_decorateur):
    """Classe représentant un enchantement de type Feu"""
    def get_description(self):

        """Retourne la description de l'objet avec l'enchantement Feu."""
        return super().get_description() + "Feu"
    
    def get_power(self):
        
        """Retourne la puissance de l'objet augmentée de 20 """
        return super().get_power() + 20