import random
from pattern.factory import Factory
from infrastructure.item_factory import ItemRegistry
from domaine.rarity import Rarity

class RandomItemFactory(Factory):
    def create(self):
        return self.random_item()

    def random_item(self):
        key = random.choice(list(ItemRegistry.keys()))
        return ItemRegistry.create(key)

    def random_by_category(self, category: str):
        filtered = ItemRegistry.filter(category=category)
        if not filtered:
            return self.random_item()
        key = random.choice(list(filtered.keys()))
        return ItemRegistry.create(key)

    def random_by_rarity(self, rarity: Rarity):
        filtered = ItemRegistry.filter(rarity=rarity)
        if not filtered:
            return self.random_item()
        key = random.choice(list(filtered.keys()))
        return ItemRegistry.create(key)

    def loot_drop(self, loot_table=None):
        if loot_table is None:
            loot_table = {
                Rarity.LEGENDAIRE: 0.10,
                Rarity.EPIC: 0.20,
                Rarity.RARE: 0.30,
                Rarity.COMMUN: 0.40
            }
        roll = random.random()
        acc = 0
        for rarity, chance in loot_table.items():
            acc += chance
            if roll <= acc:
                return self.random_by_rarity(rarity)
        return self.random_item()
