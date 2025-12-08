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
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            damage INTEGER,
            range INTEGER,
            defense INTEGER,
            rarity TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            type TEXT NOT NULL
        );
    ''')
    conn.commit()
    conn.close()