from enum import Enum

class Rarity(Enum):
    COMMUN = "Commun"
    RARE = "Rare"
    EPIC = "Epic"
    LEGENDAIRE = "Légendaire"

    def get_color_code(self):
        return {
            Rarity.COMMUN: "\033[37m",
            Rarity.RARE: "\033[34m",
            Rarity.EPIC: "\033[35m",
            Rarity.LEGENDAIRE: "\033[33m"
        }[self]

    @staticmethod
    def reset_color():
        return "\033[0m"
