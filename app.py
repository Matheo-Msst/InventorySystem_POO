from infrastructure.database import init_db
from service.equipement_repository import ajouter_equipement, charger_equipements
from Domain.armes import Arme
from Domain.armures import Armure


def peupler_donnees_de_test():
    """Crée quelques équipements et les enregistre dans la base."""
    print("➕ Ajout d'équipements de test...")

    epee_fer = Arme(nom="Épée en fer", degats=10, portee=2, rarete="commun")
    arc_bois = Arme(nom="Arc en bois", degats=7, portee=5, rarete="rare")
    plastron_cuir = Armure(nom="Plastron en cuir", defense=5, rarete="commun")
    bouclier_acier = Armure(nom="Bouclier en acier", defense=12, rarete="épique")

    ajouter_equipement(epee_fer, quantite=1)
    ajouter_equipement(arc_bois, quantite=2)
    ajouter_equipement(plastron_cuir, quantite=1)
    ajouter_equipement(bouclier_acier, quantite=1)

    print("✅ Données de test ajoutées.\n")


def afficher_inventaire():
    """Charge et affiche tout l'inventaire stocké en BDD."""
    print("📦 Inventaire actuel :")
    equipements = charger_equipements()

    if not equipements:
        print("  (inventaire vide)")
        return

    for equipement, quantite in equipements:
        # equipement est une instance de Arme ou Armure (hérite de Equipement)
        print(f"- {equipement} x{quantite}")


def main():
    # 1) Initialiser la base (crée la table si besoin)
    print("🚀 Initialisation de la base de données...")
    init_db()
    print("✅ Base initialisée.\n")

    # 2) Ajouter des données de test
    peupler_donnees_de_test()

    # 3) Afficher ce qu'il y a dans l'inventaire
    afficher_inventaire()


if __name__ == "__main__":
    main()
