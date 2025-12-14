import random
from models.item_types.armes import Weapon
from models.item_types.rareter import Rareter


AVAILABLE_WEAPONS = [
    "Épée en bois",
    "Dague de fer",
    "Hache simple",
    "Bâton de combat",
    "Lance en bois",
    
    "Épée d'acier",
    "Hache de guerre",
    "Arc en ébène",
    "Marteau légendaire",
    
    "Excalibur",
    "Mjolnir",
    "Lame des dragons",
]


class ChestService:
    """Service pour gérer l'ouverture de coffres et la génération d'armes aléatoires"""
    
    def generate_random_weapon(self):
        """
        Génère une arme aléatoire basée sur les chances de rareté
        
        Returns:
            Weapon: Une arme avec rareté aléatoire (sans ID, sera assigné par la BD)
        """
        rand = random.random()
        
        if rand < Rareter.COMMUN.chance_drop():  # 0-0.70
            rarity = Rareter.COMMUN
            weapon_names = AVAILABLE_WEAPONS[0:5]
        elif rand < Rareter.COMMUN.chance_drop() + Rareter.RARE.chance_drop():  # 0.70-0.95
            rarity = Rareter.RARE
            weapon_names = AVAILABLE_WEAPONS[5:9]
        else:  # 0.95-1.00
            rarity = Rareter.EPIC
            weapon_names = AVAILABLE_WEAPONS[9:12]
        
        weapon_name = random.choice(weapon_names)
        
        weapon = Weapon(0, weapon_name, rarity)
        
        return weapon
    
    def get_drop_info(self):
        """Retourne les informations de drop pour affichage"""
        return {
            "COMMUN": {
                "name": "Commun",
                "chance": f"{int(Rareter.COMMUN.chance_drop() * 100)}%",
                "color": "white"
            },
            "RARE": {
                "name": "Rare",
                "chance": f"{int(Rareter.RARE.chance_drop() * 100)}%",
                "color": "green"
            },
            "EPIC": {
                "name": "Épique",
                "chance": f"{int(Rareter.EPIC.chance_drop() * 100)}%",
                "color": "gold"
            }
        }
