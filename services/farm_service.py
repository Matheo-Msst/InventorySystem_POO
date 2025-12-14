import random
from models.item_types.ressource import Resource, RessourceType


class FarmService:
    """Service pour la génération aléatoire de ressources lors du farming"""

    # Ressources disponibles au farming
    AVAILABLE_RESOURCES = [
        RessourceType.BOIS,
        RessourceType.PIERRE,
        RessourceType.CHARBON,
        RessourceType.FER,
        RessourceType.OR,
        RessourceType.DIAMANT,
    ]

    # Distribution de probabilité (doit totaliser 100%)
    RESOURCE_PROBABILITIES = {
        RessourceType.BOIS: 0.30,      # 30% - Très commun
        RessourceType.PIERRE: 0.25,    # 25% - Commun
        RessourceType.CHARBON: 0.20,   # 20% - Assez commun
        RessourceType.FER: 0.15,       # 15% - Moyen
        RessourceType.OR: 0.07,        # 7% - Rare
        RessourceType.DIAMANT: 0.03,   # 3% - Très rare
    }

    # Quantités générées selon le type (aléatoire entre min et max)
    RESOURCE_QUANTITIES = {
        RessourceType.BOIS: (4, 12),       # 4-12 bois
        RessourceType.PIERRE: (3, 10),     # 3-10 pierre
        RessourceType.CHARBON: (2, 8),     # 2-8 charbon
        RessourceType.FER: (1, 5),         # 1-5 fer
        RessourceType.OR: (1, 3),          # 1-3 or
        RessourceType.DIAMANT: (1, 1),     # 1 diamant (toujours 1)
    }

    def generate_random_resource(self) -> Resource:
        """
        Génère une ressource aléatoire basée sur les probabilités

        Returns:
            Resource: Une ressource avec type et quantité aléatoires
        """
        # Générer un nombre aléatoire entre 0 et 1
        rand = random.random()

        # Déterminer le type de ressource basé sur les probabilités cumulées
        cumulative_prob = 0
        selected_resource_type = RessourceType.BOIS  # Default

        for resource_type, probability in self.RESOURCE_PROBABILITIES.items():
            cumulative_prob += probability
            if rand < cumulative_prob:
                selected_resource_type = resource_type
                break

        # Générer une quantité aléatoire pour ce type
        min_qty, max_qty = self.RESOURCE_QUANTITIES[selected_resource_type]
        quantity = random.randint(min_qty, max_qty)

        # Créer la ressource (ID = 0, sera assigné par la BD)
        resource = Resource(0, selected_resource_type, quantity)

        return resource

    def get_farming_info(self):
        """Retourne les informations de farming pour affichage (taux de drop)"""
        return {
            resource_type.name: {
                "name": resource_type.get_name(),
                "emoji": resource_type.get_emoji(),
                "chance": f"{int(self.RESOURCE_PROBABILITIES[resource_type] * 100)}%",
                "color": resource_type.get_color(),
                "max_stack": resource_type.get_max_stack(),
                "quantity_range": f"{self.RESOURCE_QUANTITIES[resource_type][0]}-{self.RESOURCE_QUANTITIES[resource_type][1]}"
            }
            for resource_type in self.AVAILABLE_RESOURCES
        }
