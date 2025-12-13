import json
import os
import random
from domaine.item import Item
from domaine.rarity import Rarity
from pattern.factory import Factory, Registry

def random_rarity():
    roll = random.random()
    if roll <= 0.05:
        return Rarity.LEGENDAIRE
    elif roll <= 0.20:
        return Rarity.EPIC
    elif roll <= 0.50:
        return Rarity.RARE
    else:
        return Rarity.COMMUN

class ItemFactory(Factory):
    def __init__(self, name: str, image: str, max_stack: int, rarity: Rarity = None):
        self.name = name
        self.image = image
        self.max_stack = max_stack
        self.rarity = rarity or random_rarity()

    def create(self) -> Item:
        return Item(self.name, self.image, self.max_stack, self.rarity)

class MaterialFactory(ItemFactory):
    def __init__(self, name: str, image: str, max_stack: int = 64):
        super().__init__(name, image, max_stack, rarity=None)

class EquipmentFactory(ItemFactory):
    def __init__(self, name: str, image: str, rarity: Rarity = None):
        super().__init__(name, image, max_stack=1, rarity=rarity)

    def create(self) -> Item:
        rarity = self.rarity or random.choice(list(Rarity))
        return Item(self.name, self.image, 1, rarity)

# Registre global
ItemRegistry = Registry()

def load_items_from_json(json_path: str = None):
    if json_path is None:
        base = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(os.path.dirname(base), 'data', 'items.json')

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Matériaux
        for mat in data.get('materials', []):
            ItemRegistry.register(mat['id'], MaterialFactory(mat['name'], mat['image'], mat.get('max_stack', 64)),
                                    {'name': mat['name'], 'category': mat.get('category', 'material')})

        # Équipements
        for eq in data.get('equipments', []):
            rarity = Rarity[eq['rarity']] if 'rarity' in eq else None
            ItemRegistry.register(eq['id'], EquipmentFactory(eq['name'], eq['image'], rarity),
                                    {'name': eq['name'], 'category': eq.get('category', 'equipment')})
    except Exception as e:
        print("⚠️ Erreur JSON:", e)

def get_all_items():
    items = ItemRegistry.all()
    return {k: (v['metadata'].get('name', k), v['factory'].create) for k, v in items.items()}

# Charger les items au démarrage
load_items_from_json()
