from flask import Blueprint, render_template, abort, request, redirect, url_for, jsonify
from services.user_service import get_all_users, get_user_by_id
from services.inventory_service import InventoryService
from services.chest_service import ChestService
from models.item import Item
from models.item_types.armes import Weapon
from models.item_types.rareter import Rareter

inv = InventoryService()
chest_service = ChestService()
items_registry = []
next_item_id = 1 

# Créer un blueprint pour les routes
routes_bp = Blueprint('routes', __name__)

@routes_bp.route("/admin", methods=["GET", "POST"])
def admin():
    global next_item_id
    users = get_all_users()

    if request.method == "POST":
        item_name = request.form.get("item_name")
        rarity_str = request.form.get("rarity", "COMMUN")  # Par défaut COMMUN
        user_id = int(request.form.get("user_id"))

        user = get_user_by_id(user_id)
        
        # Convertir la string en enum Rareter
        try:
            rarity = Rareter[rarity_str.upper()]
        except KeyError:
            rarity = Rareter.COMMUN
        
        # Créer une Weapon avec la rareté
        new_weapon = Weapon(next_item_id, item_name, rarity, user)
        next_item_id += 1
        items_registry.append(new_weapon)

        for c, slot in enumerate(user.inventory[0]):
            if slot == "":
                user.inventory[0][c] = new_weapon
                new_weapon.col = c
                break

        return redirect(url_for("routes.admin"))

    return render_template("admin.html", users=users, items=items_registry, rarities=Rareter)


@routes_bp.route("/")
def home():
    users = get_all_users()
    return render_template("index.html", users=users)


@routes_bp.route("/user/<int:user_id>")
def user_page(user_id):
    user = get_user_by_id(user_id)
    if not user:
        return "Utilisateur introuvable", 404

    return render_template("inventoryUser.html", user=user)


@routes_bp.route("/chest/<int:user_id>")
def chest_page(user_id):
    """Affiche la page du coffre"""
    user = get_user_by_id(user_id)
    if not user:
        return "Utilisateur introuvable", 404
    
    drop_info = chest_service.get_drop_info()
    return render_template("chest.html", user=user, drop_info=drop_info)


@routes_bp.route("/api/open-chest/<int:user_id>", methods=["POST"])
def open_chest(user_id):
    """API: Ouvre un coffre et génère une arme aléatoire"""
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "Utilisateur introuvable"}), 404
    
    # Générer une arme aléatoire
    weapon = chest_service.generate_random_weapon(next_item_id)
    weapon.user = user
    items_registry.append(weapon)
    
    # Chercher un slot vide dans l'inventaire
    for c, slot in enumerate(user.inventory[0]):
        if slot == "":
            user.inventory[0][c] = weapon
            weapon.col = c
            
            return jsonify({
                "success": True,
                "weapon": {
                    "id": weapon.id,
                    "name": weapon.name,
                    "rarity": weapon.rarity.name,
                    "rarity_display": weapon.get_rarity_name(),
                    "color": weapon.get_rarity_color()
                }
            }), 200
    
    # Inventaire plein
    return jsonify({"error": "Inventaire plein! Veuillez libérer un slot."}), 400
