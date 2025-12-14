import sqlite3

DB_PATH = 'inventory.db'

def get_connexion():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connexion()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE
        );
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weapons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            rarity TEXT NOT NULL,
            user_id INTEGER,
            col INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resource_type TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            user_id INTEGER,
            col INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    ''')
    
    conn.commit()
    conn.close()


# ===== FONCTIONS UTILISATEURS =====

def get_all_users():
    """Récupère tous les utilisateurs de la BD"""
    conn = get_connexion()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    return users

def get_user_by_id(user_id):
    """Récupère un utilisateur par son ID"""
    conn = get_connexion()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def create_user(user_id, name):
    """Crée un nouvel utilisateur"""
    conn = get_connexion()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (id, name) VALUES (?, ?)', (user_id, name))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


# ===== FONCTIONS ARMES/ITEMS =====

def get_all_weapons():
    """Récupère toutes les armes"""
    conn = get_connexion()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM weapons')
    weapons = cursor.fetchall()
    conn.close()
    return weapons

def get_user_weapons(user_id):
    """Récupère toutes les armes d'un utilisateur"""
    conn = get_connexion()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM weapons WHERE user_id = ? ORDER BY col', (user_id,))
    weapons = cursor.fetchall()
    conn.close()
    return weapons

def create_weapon(name, rarity, user_id, col=None):
    """Crée une nouvelle arme"""
    conn = get_connexion()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO weapons (name, rarity, user_id, col) VALUES (?, ?, ?, ?)',
        (name, rarity, user_id, col)
    )
    conn.commit()
    weapon_id = cursor.lastrowid
    conn.close()
    return weapon_id

def update_weapon(weapon_id, user_id=None, col=None):
    """Met à jour une arme"""
    conn = get_connexion()
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE weapons SET user_id = ?, col = ? WHERE id = ?',
        (user_id, col, weapon_id)
    )
    conn.commit()
    conn.close()

def delete_weapon(weapon_id):
    """Supprime une arme"""
    conn = get_connexion()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM weapons WHERE id = ?', (weapon_id,))
    conn.commit()
    conn.close()

def get_weapon_by_id(weapon_id):
    """Récupère une arme par son ID"""
    conn = get_connexion()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM weapons WHERE id = ?', (weapon_id,))
    weapon = cursor.fetchone()
    conn.close()
    return weapon

def find_empty_slot(user_id):
    """Trouve le premier slot vide pour un utilisateur (0-8), en regardant ARMES ET RESSOURCES"""
    conn = get_connexion()
    cursor = conn.cursor()
    for col in range(9):
        # Vérifier si le slot est occupé par une arme
        cursor.execute('SELECT * FROM weapons WHERE user_id = ? AND col = ?', (user_id, col))
        if cursor.fetchone() is not None:
            continue
        
        # Vérifier si le slot est occupé par une ressource
        cursor.execute('SELECT * FROM resources WHERE user_id = ? AND col = ?', (user_id, col))
        if cursor.fetchone() is not None:
            continue
        
        # Le slot est vide
        conn.close()
        return col
    
    conn.close()
    return None  # Inventaire plein


# ===== FONCTIONS RESSOURCES =====

def get_all_resources():
    """Récupère toutes les ressources"""
    conn = get_connexion()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM resources')
    resources = cursor.fetchall()
    conn.close()
    return resources

def get_user_resources(user_id):
    """Récupère toutes les ressources d'un utilisateur"""
    conn = get_connexion()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM resources WHERE user_id = ? ORDER BY col', (user_id,))
    resources = cursor.fetchall()
    conn.close()
    return resources

def create_resource(resource_type, quantity, user_id, col=None):
    """
    Crée une nouvelle ressource
    
    Args:
        resource_type: Type de ressource (enum name, ex: "BOIS")
        quantity: Quantité de ressources
        user_id: ID de l'utilisateur propriétaire
        col: Emplacement dans l'inventaire (optionnel)
    
    Returns:
        ID de la ressource créée
    """
    conn = get_connexion()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO resources (resource_type, quantity, user_id, col) VALUES (?, ?, ?, ?)',
        (resource_type, quantity, user_id, col)
    )
    conn.commit()
    resource_id = cursor.lastrowid
    conn.close()
    return resource_id

def update_resource(resource_id, quantity=None, col=None, user_id=None):
    """Met à jour une ressource"""
    conn = get_connexion()
    cursor = conn.cursor()
    
    if quantity is not None and col is not None and user_id is not None:
        cursor.execute(
            'UPDATE resources SET quantity = ?, col = ?, user_id = ? WHERE id = ?',
            (quantity, col, user_id, resource_id)
        )
    elif quantity is not None:
        cursor.execute('UPDATE resources SET quantity = ? WHERE id = ?', (quantity, resource_id))
    elif col is not None:
        cursor.execute('UPDATE resources SET col = ? WHERE id = ?', (col, resource_id))
    
    conn.commit()
    conn.close()

def delete_resource(resource_id):
    """Supprime une ressource"""
    conn = get_connexion()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM resources WHERE id = ?', (resource_id,))
    conn.commit()
    conn.close()

def get_resource_by_id(resource_id):
    """Récupère une ressource par son ID"""
    conn = get_connexion()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM resources WHERE id = ?', (resource_id,))
    resource = cursor.fetchone()
    conn.close()
    return resource

def find_stackable_resource_slot(user_id, resource_type):
    """
    Trouve un slot contenant une ressource du même type non pleine
    Retourne (col, id, current_quantity) ou (None, None, None) si aucun trouvé
    """
    conn = get_connexion()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT id, col, quantity FROM resources WHERE user_id = ? AND resource_type = ? ORDER BY col',
        (user_id, resource_type)
    )
    resources = cursor.fetchall()
    
    for resource_row in resources:
        # Récupérer le max_stack depuis le type de ressource
        from models.item_types.ressource import RessourceType
        max_stack = RessourceType[resource_type].get_max_stack()
        
        if resource_row['quantity'] < max_stack:
            conn.close()
            return (resource_row['col'], resource_row['id'], resource_row['quantity'])
    
    conn.close()
    return (None, None, None)

def find_empty_resource_slot(user_id):
    """Trouve le premier slot vide pour une ressource (regarde armes ET ressources)"""
    conn = get_connexion()
    cursor = conn.cursor()
    
    for col in range(9):
        # Vérifier si le slot est occupé par une arme
        cursor.execute('SELECT * FROM weapons WHERE user_id = ? AND col = ?', (user_id, col))
        if cursor.fetchone() is not None:
            continue
        
        # Vérifier si le slot est occupé par une ressource
        cursor.execute('SELECT * FROM resources WHERE user_id = ? AND col = ?', (user_id, col))
        if cursor.fetchone() is None:
            conn.close()
            return col
    
    conn.close()
    return None  # Inventaire plein