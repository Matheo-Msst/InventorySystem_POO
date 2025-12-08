from services.database import get_connexion
from models.item.equipement import Equipement
from models.item.armes import Arme
from models.item.armures import Armure

def ajouter_equipement(equipement: Equipement, quantite: int):
    conn = get_connexion()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO inventory (name, damage, range, defense, rarity, quantity, type)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        equipement.nom,
        getattr(equipement, 'degats', None),
        getattr(equipement, 'portee', None),
        getattr(equipement, 'defense', None),
        equipement.rarete,
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
            equip = Arme(
                nom=row['name'],
                degats=row['damage'],
                portee=row['range'],
                rarete=row['rarity']
            )
        elif row['type'] == 'armure':
            equip = Armure(
                nom=row['name'],
                defense=row['defense'],
                rarete=row['rarity']
            )
        else:
            continue

        equipements.append((equip, row['quantity']))

    conn.close()
    return equipements
