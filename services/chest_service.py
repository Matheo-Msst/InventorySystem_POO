import random
from models.item_types.armes import Weapon
from models.item_types.rareter import Rareter


# Liste d'armes disponibles dans le coffre
AVAILABLE_WEAPONS = [
    # Armes Communes (70% de chance)
    "Épée en bois",
    "Dague de fer",
    "Hache simple",
    "Bâton de combat",
    "Lance en bois",
    
    # Armes Rares (25% de chance)
    "Épée d'acier",
    "Hache de guerre",
    "Arc en ébène",
    "Marteau légendaire",
    
    # Armes Épiques (5% de chance)
    "Excalibur",
    "Mjolnir",
    "Lame des dragons",
]


class ChestService:
    """Service pour gérer l'ouverture de coffres et la génération d'armes aléatoires"""
    
    def __init__(self):
        self.next_weapon_id = 1
    
    def generate_random_weapon(self, current_id=None):
        """
        Génère une arme aléatoire basée sur les chances de rareté
        
        Args:
            current_id: ID à utiliser pour l'arme (optionnel)
        
        Returns:
            Weapon: Une arme avec rareté aléatoire
        """
        # Générer un nombre aléatoire entre 0 et 1
        rand = random.random()
        
        # Déterminer la rareté basée sur les chances cumulées
        if rand < Rareter.COMMUN.chance_drop():  # 0-0.70
            rarity = Rareter.COMMUN
            # Choisir une arme commune
            weapon_names = AVAILABLE_WEAPONS[0:5]
        elif rand < Rareter.COMMUN.chance_drop() + Rareter.RARE.chance_drop():  # 0.70-0.95
            rarity = Rareter.RARE
            # Choisir une arme rare
            weapon_names = AVAILABLE_WEAPONS[5:9]
        else:  # 0.95-1.00
            rarity = Rareter.EPIC
            # Choisir une arme épique
            weapon_names = AVAILABLE_WEAPONS[9:12]
        
        # Sélectionner une arme aléatoire de la rareté choisie
        weapon_name = random.choice(weapon_names)
        
        # Créer l'objet Weapon
        weapon_id = current_id if current_id else self.next_weapon_id
        self.next_weapon_id = max(self.next_weapon_id, weapon_id + 1)
        
        weapon = Weapon(weapon_id, weapon_name, rarity)
        
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
