from flask import Blueprint, render_template, abort, request, redirect, url_for, jsonify
from services.user_service import get_all_users, get_user_by_id
from services.inventory_service import InventoryService
from services.chest_service import ChestService
from services import database as db
from models.item import Item
from models.item_types.armes import Weapon
from models.item_types.rareter import Rareter

inv = InventoryService()
chest_service = ChestService()

routes_bp = Blueprint('routes', __name__)

@routes_bp.route("/admin", methods=["GET", "POST"])
def admin():
    users = get_all_users()

    if request.method == "POST":
        item_name = request.form.get("item_name")
        rarity_str = request.form.get("rarity", "COMMUN")  
        user_id = int(request.form.get("user_id"))

        try:
            rarity_enum = Rareter[rarity_str.upper()]
            rarity_name = rarity_enum.name
        except KeyError:
            rarity_name = "COMMUN"
        
        empty_slot = db.find_empty_slot(user_id)
        db.create_weapon(item_name, rarity_name, user_id, empty_slot)

        return redirect(url_for("routes.admin"))

    all_weapons_rows = db.get_all_weapons()
    all_weapons = []
    
    for weapon_row in all_weapons_rows:
        try:
            rarity = Rareter[weapon_row['rarity']]
        except KeyError:
            rarity = Rareter.COMMUN
        
        weapon = Weapon(weapon_row['id'], weapon_row['name'], rarity)
        weapon.col = weapon_row['col']
        weapon.user = get_user_by_id(weapon_row['user_id']) if weapon_row['user_id'] else None
        all_weapons.append(weapon)
    
    return render_template("admin.html", users=users, items=all_weapons, rarities=Rareter)


@routes_bp.route("/")
def home():
    users = get_all_users()
    return render_template("index.html", users=users)


@routes_bp.route("/user/<int:user_id>")
def user_page(user_id):
    user = get_user_by_id(user_id)
    if not user:
        return "Utilisateur introuvable", 404

    user_weapons = db.get_user_weapons(user_id)
    
    inventory = [""] * 9
    for weapon_row in user_weapons:
        if weapon_row['col'] is not None and 0 <= weapon_row['col'] < 9:
            try:
                rarity = Rareter[weapon_row['rarity']]
            except KeyError:
                rarity = Rareter.COMMUN
            
            weapon = Weapon(weapon_row['id'], weapon_row['name'], rarity)
            inventory[weapon_row['col']] = weapon
    
    user.inventory = [inventory]
    
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
    
    empty_slot = db.find_empty_slot(user_id)
    if empty_slot is None:
        return jsonify({"error": "Inventaire plein! Veuillez libérer un slot."}), 400
    
    weapon = chest_service.generate_random_weapon()
    
    weapon_id = db.create_weapon(weapon.name, weapon.rarity.name, user_id, empty_slot)
    
    return jsonify({
        "success": True,
        "weapon": {
            "id": weapon_id,
            "name": weapon.name,
            "rarity": weapon.rarity.name,
            "rarity_display": weapon.get_rarity_name(),
            "color": weapon.get_rarity_color()
        }
    }), 200
