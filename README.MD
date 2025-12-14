# 🎮 Inventory System POO

> Système de gestion d'inventaire avec coffre de loot aléatoire - Projet étudiant YNOV

---

## 🎯 À propos

**Inventory System POO** est une application web de gestion d'inventaire développée en Python avec Flask. Le système permet aux utilisateurs de gérer une grille d'inventaire (3×3) et d'ouvrir des coffres pour recevoir des armes aléatoires avec différents niveaux de rareté.

Ce projet démontre l'application pratique des principes de la **Programmation Orientée Objet (POO)** dans un contexte web moderne.

---

## 👥 Équipe

| Rôle | Membres |
|------|---------|
| **Nom d'équipe** | Teddy Beer 🍺 |
| **Développeurs** | Victoria, Mathéo, Hugo, Teddy |
| **École** | YNOV |

---

## 💻 Technologies

| Domaine | Technologie |
|---------|------------|
| **Backend** | Python 3.13 |
| **Framework web** | Flask |
| **Base de données** | SQLite |
| **Frontend** | HTML5, CSS3, JavaScript |
| **Gestion de version** | Git/GitHub |

---

## 🏗️ Architecture

### Modèle MVC (Model-View-Controller)

```
InventorySystem_POO/
├── models/                 # Couche Modèle
│   ├── item.py            # Classe Item de base
│   ├── user_model.py      # Classe User
│   └── item_types/        # Sous-domaine des types d'armes
│       ├── armes.py       # Classe Weapon
│       └── rareter.py     # Énumération des raretés
│
├── services/              # Couche Logique métier
│   ├── database.py        # Gestion SQLite et CRUD
│   ├── user_service.py    # Services utilisateurs
│   ├── inventory_service.py # Services inventaire
│   ├── chest_service.py   # Services coffre & loot
│   └── routes.py          # Routes Flask (Controller)
│
├── templates/             # Couche Présentation (View)
│   ├── index.html         # Accueil & liste utilisateurs
│   ├── inventoryUser.html # Inventaire personnel
│   ├── chest.html         # Interface du coffre
│   └── admin.html         # Panel administrateur
│
├── static/
│   └── style.css          # Feuille de style centralisée
│
└── app.py                 # Point d'entrée Flask
```

---

## 🚀 Installation

### Prérequis

- Python 3.10+
- pip (gestionnaire de paquets Python)

### Étapes

1. **Cloner le dépôt**
```bash
git clone https://github.com/Matheo-Msst/InventorySystem_POO.git
cd InventorySystem_POO
```

2. **Créer un environnement virtuel** (recommandé)
```bash
python -m venv venv
# Sur Windows
venv\Scripts\activate
# Sur macOS/Linux
source venv/bin/activate
```

3. **Installer les dépendances**
```bash
pip install flask
```

4. **Initialiser la base de données**
```bash
python app.py
# La base de données `inventory.db` sera créée automatiquement
```

---

## ▶️ Utilisation

### Lancer l'application

```bash
python app.py
```

L'application sera accessible à : **http://127.0.0.1:5000**

### Points d'accès principaux

| Route | Description |
|-------|-------------|
| `/` | **Accueil** - Liste de tous les utilisateurs |
| `/user/<id>` | **Inventaire** - Grille 3×3 de l'utilisateur |
| `/chest/<id>` | **Coffre** - Interface pour ouvrir un coffre |
| `/admin` | **Panel Admin** - Créer manuellement des armes |

---

## ✨ Fonctionnalités

### 🎒 Gestion d'inventaire
- Grille d'inventaire **3×3** (9 emplacements)
- Affichage des armes avec **nom** et **rareté**
- Prise en charge des emplacements vides
- **Persistance** via SQLite

### 🏺 Système de coffre
- Génération aléatoire d'armes
- Système de **rareté** probabiliste :
  - 🟡 **Commun** : 70%
  - 🟢 **Rare** : 25%
  - ⭐ **Épique** : 5%
- Interface visuelle avec animations
- **Vérification** des emplacements avant ajout

### ⚔️ Gestion d'armes
- Création d'armes avec rareté sélectionnable
- Affichage en couleur selon la rareté
- Attribution automatique à un utilisateur
- Placement intelligent dans le premier slot vide

### 🔧 Panel administrateur
- Créer des armes manuellement
- Sélectionner la rareté
- Assigner à un utilisateur
- Visualiser toutes les armes créées

---

## 📝 Exemple d'utilisation

### Scénario : Un utilisateur ouvre un coffre

1. **Utilisateur navigue** vers `/chest/1`
2. **Clic sur le bouton** "Ouvrir le coffre"
3. **Requête POST** vers `/api/open-chest/1`
4. **ChestService** :
   - Génère nombre aléatoire (0-1)
   - Détermine rareté (70%, 25%, 5%)
   - Sélectionne arme du groupe
5. **Routes** :
   - Vérifie emplacement libre
   - Sauvegarde dans `inventory.db`
6. **Réponse JSON** avec détails de l'arme
7. **Frontend** affiche animation + mise à jour inventaire


