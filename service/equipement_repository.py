from infrastructure.database import get_connexion
from Domain.equipement import Equipement
from Domain.armes import Arme
from Domain.armures import Armure

def ajouter_equipement(equipement: Equipement, quantite: int):
    conn = get_connexion()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO inventory (name, damage, range, defense, rarity, quantity, type)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        equipement.nom,
        getattr(equipement.equipement_specifique, 'degats', None),
        getattr(equipement.equipement_specifique, 'portee', None),
        getattr(equipement.equipement_specifique, 'defense', None),
        equipement.equipement_specifique.rarete,
        quantite,
        equipement.type_equipement
    ))
    conn.commit()
    conn.close()

def charger_equipements():
    conn = get_connexion()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM inventory')
    rows = cursor.fetchall()
    equipements = []

    for row in rows:
        if row['type'] == 'arme':
            equipement_specifique = Arme(
                nom=row['name'],
                degats=row['damage'],
                portee=row['range'],
                rarete=row['rarity']
            )
        elif row['type'] == 'armure':
            equipement_specifique = Armure(
                nom=row['name'],
                defense=row['defense'],
                rarete=row['rarity']
            )
        equipement = Equipement(nom=row['name'], type_equipement=row['type'])
        equipement.equipement_specifique = equipement_specifique
        equipements.append((equipement, row['quantity']))

    conn.close()
    return equipements