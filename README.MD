# 🎮 InventorySystem RPG

**Un système d'inventaire complet pour jeu de rôle fantasy - Simple à utiliser !**

> **Projet Académique** - Groupe B2 Informatique YNOV Bordeaux  
> Auteurs : **Hugo**, **Victoria**, **Mathéo**, **Teddy**  
> Année : 2025

---

## 📋 Table des matières

- [Qu'est-ce que c'est ?](#-quest-ce-que-cest-)
- [Comment ça marche ?](#-comment-ça-marche-)
- [Installation (facile)](#-installation-facile)
- [Guide d'utilisation](#-guide-dutilisation)
- [Contributeurs](#-contributeurs)

---

## 👁️ Qu'est-ce que c'est ?

**InventorySystem RPG** est une application web pour gérer l'inventaire de personnages de jeu de rôle. Vous pouvez :

- 📦 **Gérer votre inventaire** : 9 emplacements pour stocker vos affaires
- 🗡️ **Collectionner des armes** : 13 armes différentes avec différentes rareté
- 🪨 **Farmer des ressources** : Bois, pierre, charbon, fer, or, diamant
- 🏪 **Ouvrir des coffres** : Récupérez des armes aléatoires
- 🌾 **Récolter** : Collectez des ressources

---

## 🎮 Comment ça marche ?

### Les pages principales

```
🏠 Accueil
   └─→ Choix du personnage

📦 Inventaire
   └─→ Voir vos armes et ressources
   └─→ Voir l'équipement par slot

🏪 Coffres
   └─→ Cliquez pour ouvrir
   └─→ Récuprez une arme aléatoire

🌾 Farming
   └─→ Cliquez pour récolter
   └─→ Récuprez une ressource aléatoire

🔧 Administration
   └─→ Ajouter manuellement des armes
   └─→ Voir tous les joueurs
```

### Les armes et leurs chances

Quand vous ouvrez un coffre, vous avez :

| Arme | Chance | Exemples |
|------|--------|----------|
| 🟩 Commune | 70% | Épée en bois, Dague de fer, Hache simple |
| 🟦 Rare | 25% | Épée d'acier, Hache de guerre, Arc en ébène |
| 🟥 Épique | 5% | Excalibur, Mjolnir, Lame des dragons |

### Les ressources à récolter

Quand vous farmez, vous pouvez obtenir :

| Ressource | Chance | Quantité |
|-----------|--------|----------|
| 🌳 Bois | 30% | 4-12 |
| 🪨 Pierre | 25% | 3-10 |
| ⚫ Charbon | 20% | 2-8 |
| ⚙️ Fer | 15% | 1-5 |
| 💛 Or | 7% | 1-3 |
| 💎 Diamant | 3% | 1 |

---

## 🚀 Installation (facile)

### Étape 1 : Télécharger le projet

Allez sur GitHub et téléchargez le projet :
https://github.com/Matheo-Msst/InventorySystem_POO

ou en ligne de commande :
```
git clone https://github.com/Matheo-Msst/InventorySystem_POO.git
```

### Étape 2 : Installer Python (si pas déjà fait)

Vous avez besoin de Python 3.10 ou plus récent. 
Téléchargez-le sur : https://www.python.org/downloads/

### Étape 3 : Ouvrir le dossier dans le terminal

Naviguez jusqu'au dossier :
```
cd InventorySystem_POO
```

### Étape 4 : Lancer l'application

Tapez simplement :
```
python app.py
```

### Étape 5 : Ouvrir dans le navigateur

Allez à cette adresse :
```
http://localhost:5000
```

**C'est tout ! L'app est prête à utiliser ! 🎉**

---

## 📖 Guide d'utilisation

### 1️⃣ Première visite - Accueil

- Vous arrivez sur la page d'accueil
- Cliquez sur le personnage que vous voulez jouer
- Vous êtes maintenant sur votre page de joueur

### 2️⃣ Voir votre inventaire

Sur votre page, vous voyez :
- **Vos armes** avec leur rareté (couleur)
- **Vos ressources** avec la quantité
- **9 emplacements** pour stocker vos affaires

Cliquez sur une arme pour voir ses détails.

### 3️⃣ Ouvrir un coffre

- Allez dans la section "Coffres"
- Cliquez sur le bouton "Ouvrir coffre"
- Une arme aléatoire vous est donnée
- Elle s'ajoute à votre inventaire

**Conseil** : Vous avez plus de chances d'avoir une arme commune, mais les épiques sont possibles !

### 4️⃣ Récolter des ressources

- Allez dans la section "Farming"
- Cliquez sur le bouton "Récolter"
- Une ressource aléatoire est ajoutée
- Elle s'ajoute à votre inventaire

**Conseil** : Le bois et la pierre sont plus faciles à trouver que le diamant !

### 5️⃣ Admin - Ajouter une arme manuellement

Si vous êtes admin :
- Allez dans la page "Administration"
- Remplissez le formulaire :
  - **Nom de l'arme** : Écrivez un nom (ex: "Épée flamboyante")
  - **Rareté** : Sélectionnez COMMUN, RARE ou EPIC
  - **Joueur** : Choisissez le personnage qui la reçoit
- Cliquez "Ajouter"
- L'arme apparaît dans l'inventaire




## 🎨 Apparence et design

### Les couleurs

- 🟩 **Vert** = Arme commune (70%)
- 🟦 **Bleu** = Arme rare (25%)
- 🟥 **Rouge** = Arme épique (5%)
- ⚫ **Gris** = Ressource

### Emojis et icônes

Chaque type d'item a son emoji pour être reconnu rapidement :
- 🗡️ Armes
- 🌳 Bois
- 🪨 Pierre
- 💎 Diamant
- etc.

---


---

## 🤝 Contributeurs

| Nom ||
|-----|------|
| **Hugo** | 
| **Victoria** | 
| **Mathéo** | 
| **Teddy** |

---

## 📞 Besoin d'aide ?

Si quelque chose ne fonctionne pas :

1. **Essayez de rafraîchir** la page (F5)
2. **Vérifiez que l'app est lancée** (python app.py)
3. **Contactez un contributeur** sur GitHub
4. **Ouvrez une "Issue"** sur le repository

---

## 🎯 Résumé ultra-rapide

```
C'est quoi ?         → Un système d'inventaire pour jeu RPG
Comment ça marche ?  → Vous ouvrez des coffres et réoltez des ressources
Comment l'utiliser ? → C'est intuitif, presque comme un jeu !
Qui peut l'utiliser ?→ N'importe qui, même sans connaître la programmation
```

---

**Créé avec ❤️ par les étudiants B2 YNOV Bordeaux - 2025**

Amusez-vous bien ! 🎮✨
