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
    """Trouve le premier slot vide pour un utilisateur (0-8)"""
    conn = get_connexion()
    cursor = conn.cursor()
    for col in range(9):
        cursor.execute('SELECT * FROM weapons WHERE user_id = ? AND col = ?', (user_id, col))
        if cursor.fetchone() is None:
            conn.close()
            return col
    conn.close()
    return None  # Inventaire plein