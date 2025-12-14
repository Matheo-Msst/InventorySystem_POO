import random
from typing import Union
from models.item_types.armes import Weapon
from models.item_types.rareter import Rareter
from models.item_types.ressource import Resource, RessourceType
from models.enchantement.enchantement_glace import IceEnchantement
from models.enchantement.enchantement_feu import FireEnchantement
       

class ItemFactory:
    
    # ===== ARMES =====
    
    AVAILABLE_WEAPONS = [
        # Armes Communes (70%)
        "Épée en bois",
        "Dague de fer",
        "Hache simple",
        "Bâton de combat",
        "Lance en bois",
        
        # Armes Rares (25%)
        "Épée d'acier",
        "Hache de guerre",
        "Arc en ébène",
        "Marteau légendaire",
        
        # Armes Épiques (5%)
        "Excalibur",
        "Mjolnir",
        "Lame des dragons",
    ]
    
    # ===== RESSOURCES =====
    
    AVAILABLE_RESOURCES = [
        RessourceType.BOIS,
        RessourceType.PIERRE,
        RessourceType.CHARBON,
        RessourceType.FER,
        RessourceType.OR,
        RessourceType.DIAMANT,
    ]
    
    RESOURCE_PROBABILITIES = {
        RessourceType.BOIS: 0.30,      # 30%
        RessourceType.PIERRE: 0.25,    # 25%
        RessourceType.CHARBON: 0.20,   # 20%
        RessourceType.FER: 0.15,       # 15%
        RessourceType.OR: 0.07,        # 7%
        RessourceType.DIAMANT: 0.03,   # 3%
    }
    
    RESOURCE_QUANTITIES = {
        RessourceType.BOIS: (4, 12),
        RessourceType.PIERRE: (3, 10),
        RessourceType.CHARBON: (2, 8),
        RessourceType.FER: (1, 5),
        RessourceType.OR: (1, 3),
        RessourceType.DIAMANT: (1, 1),
    }
    
    @staticmethod
    def create_random_weapon() -> Weapon:
        rand = random.random()
        
        if rand < Rareter.COMMUN.chance_drop():  # 0-0.70
            rarity = Rareter.COMMUN
            weapon_names = ItemFactory.AVAILABLE_WEAPONS[0:5]
        elif rand < Rareter.COMMUN.chance_drop() + Rareter.RARE.chance_drop():  # 0.70-0.95
            rarity = Rareter.RARE
            weapon_names = ItemFactory.AVAILABLE_WEAPONS[5:9]
        else:  # 0.95-1.00
            rarity = Rareter.EPIC
            weapon_names = ItemFactory.AVAILABLE_WEAPONS[9:12]
        
        weapon_name = random.choice(weapon_names)
        
    
        weapon = Weapon(0, weapon_name, rarity)

        weapon.enchantements = []

        # Enchantements aléatoires
        if random.random() < 0.6:
            weapon = FireEnchantement(weapon)
            weapon.enchantements.append("Feu")  

        if random.random() < 0.3:
            weapon = IceEnchantement(weapon)
            weapon.enchantements.append("Glace")

        return weapon
    
    @staticmethod
    def create_weapon(item_id: int, name: str, rarity: Rareter, user=None, col=None) -> Weapon:
        if not name or len(name.strip()) == 0:
            raise ValueError("Le nom de l'arme ne peut pas être vide")
        
        if not isinstance(rarity, Rareter):
            raise ValueError("La rareté doit être un enum Rareter")
        
        return Weapon(item_id, name, rarity, user, col)
    
    @staticmethod
    def create_weapon_from_db(weapon_row: dict) -> Weapon:
        try:
            rarity = Rareter[weapon_row['rarity']]
        except KeyError:
            rarity = Rareter.COMMUN
        
        weapon = Weapon(
            weapon_row['id'],
            weapon_row['name'],
            rarity,
            col=weapon_row['col']
        )
        return weapon
    
    

 
    # ===== RESSOURCES =====
    
    @staticmethod
    def create_random_resource() -> Resource:
        rand = random.random()
        
        cumulative_prob = 0
        selected_resource_type = RessourceType.BOIS
        
        for resource_type, probability in ItemFactory.RESOURCE_PROBABILITIES.items():
            cumulative_prob += probability
            if rand < cumulative_prob:
                selected_resource_type = resource_type
                break
        
        min_qty, max_qty = ItemFactory.RESOURCE_QUANTITIES[selected_resource_type]
        quantity = random.randint(min_qty, max_qty)
        
        return Resource(0, selected_resource_type, quantity)
    
    @staticmethod
    def create_resource(item_id: int, resource_type: RessourceType, 
                       quantity: int, user=None, col=None) -> Resource:

        if not isinstance(resource_type, RessourceType):
            raise ValueError("Le type doit être un enum RessourceType")
        
        if quantity < 1:
            raise ValueError("La quantité doit être au moins 1")
        
        return Resource(item_id, resource_type, quantity, col, user)
    
    @staticmethod
    def create_resource_from_db(resource_row: dict) -> Resource:
        try:
            resource_type = RessourceType[resource_row['resource_type']]
        except KeyError:
            raise ValueError(f"Type de ressource invalide: {resource_row['resource_type']}")
        
        resource = Resource(
            resource_row['id'],
            resource_type,
            resource_row['quantity'],
            col=resource_row['col']
        )
        return resource
    
    # ===== UTILITAIRES =====
    
    @staticmethod
    def get_weapon_drop_info() -> dict:
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
    
    @staticmethod
    def get_resource_farming_info() -> dict:

        return {
            resource_type.name: {
                "name": resource_type.get_name(),
                "emoji": resource_type.get_emoji(),
                "chance": f"{int(ItemFactory.RESOURCE_PROBABILITIES[resource_type] * 100)}%",
                "color": resource_type.get_color(),
                "max_stack": resource_type.get_max_stack(),
                "quantity_range": f"{ItemFactory.RESOURCE_QUANTITIES[resource_type][0]}-{ItemFactory.RESOURCE_QUANTITIES[resource_type][1]}"
            }
            for resource_type in ItemFactory.AVAILABLE_RESOURCES
        }
