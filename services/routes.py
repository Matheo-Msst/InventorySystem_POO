from flask import Blueprint, render_template, abort, request, redirect, url_for, jsonify
from services.user_service import get_all_users, get_user_by_id
from services.inventory_service import InventoryService
from services import database as db
from models.item import Item
from models.item_types.armes import Weapon
from models.item_types.rareter import Rareter
from models.item_types.ressource import Resource, RessourceType
from pattern.item_factory import ItemFactory

inv = InventoryService()

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
        weapon = ItemFactory.create_weapon_from_db(weapon_row)
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
    user_resources = db.get_user_resources(user_id)
    
    inventory = [""] * 9
    
    for weapon_row in user_weapons:
        if weapon_row['col'] is not None and 0 <= weapon_row['col'] < 9:
            weapon = ItemFactory.create_weapon_from_db(weapon_row)
            inventory[weapon_row['col']] = weapon
    
    for resource_row in user_resources:
        resource = ItemFactory.create_resource_from_db(resource_row)
        if resource is None:
            continue
        
        if resource_row['col'] is not None and 0 <= resource_row['col'] < 9:
            if inventory[resource_row['col']] == "":
                inventory[resource_row['col']] = resource
            else:
                placed = False
                for i in range(9):
                    if inventory[i] == "":
                        inventory[i] = resource
                        db.update_resource(resource_row['id'], col=i)
                        placed = True
                        break
                if not placed:
                    pass
        else:
            for i in range(9):
                if inventory[i] == "":
                    inventory[i] = resource
                    db.update_resource(resource_row['id'], col=i)
                    break
    
    user.inventory = [inventory]
    
    return render_template("inventoryUser.html", user=user)


@routes_bp.route("/chest/<int:user_id>")
def chest_page(user_id):
    """Affiche la page du coffre"""
    user = get_user_by_id(user_id)
    if not user:
        return "Utilisateur introuvable", 404
    
    drop_info = ItemFactory.get_weapon_drop_info()
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
    
    weapon = ItemFactory.create_random_weapon()
    
    weapon_id = db.create_weapon(weapon.name, weapon.rarity.name, user_id, empty_slot)
    
    return jsonify({
        "success": True,
        "weapon": {
            "id": weapon_id,
            "name": weapon.name,
            "rarity": weapon.rarity.name,
            "rarity_display": weapon.get_rarity_name(),
            "color": weapon.get_rarity_color(),
            "enchantements": weapon.enchantements
        }
    }), 200


@routes_bp.route("/farm/<int:user_id>")
def farm_page(user_id):
    """Affiche la page du farming"""
    user = get_user_by_id(user_id)
    if not user:
        return "Utilisateur introuvable", 404
    
    farming_info = ItemFactory.get_resource_farming_info()
    return render_template("farm.html", user=user, farming_info=farming_info)


@routes_bp.route("/api/farm/<int:user_id>", methods=["POST"])
def farm_resource(user_id):
    """API: Farm une ressource aléatoire"""
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "Utilisateur introuvable"}), 404
    
    resource = ItemFactory.create_random_resource()
    resource_type = resource.resource_type.name
    quantity = resource.quantity
    max_stack = resource.get_max_stack()
    
    stackable_col, stackable_id, current_qty = db.find_stackable_resource_slot(user_id, resource_type)
    
    if stackable_col is not None:
        new_quantity = current_qty + quantity
        
        if new_quantity <= max_stack:
            db.update_resource(stackable_id, quantity=new_quantity)
            return jsonify({
                "success": True,
                "type": "stack_update",
                "resource": {
                    "id": stackable_id,
                    "type": resource_type,
                    "quantity": new_quantity,
                    "max_stack": max_stack,
                    "emoji": resource.get_emoji(),
                    "name": resource.name,
                    "color": resource.get_color()
                }
            }), 200
        else:
            overflow = new_quantity - max_stack
            db.update_resource(stackable_id, quantity=max_stack)
            
            empty_col = db.find_empty_resource_slot(user_id)
            if empty_col is not None:
                resource_id = db.create_resource(resource_type, overflow, user_id, empty_col)
                return jsonify({
                    "success": True,
                    "type": "stack_overflow",
                    "updated_resource": {
                        "id": stackable_id,
                        "type": resource_type,
                        "quantity": max_stack,
                        "max_stack": max_stack
                    },
                    "new_resource": {
                        "id": resource_id,
                        "type": resource_type,
                        "quantity": overflow,
                        "max_stack": max_stack,
                        "emoji": resource.get_emoji(),
                        "name": resource.name,
                        "color": resource.get_color(),
                        "col": empty_col
                    }
                }), 200
            else:
                return jsonify({"error": "Inventaire plein! Veuillez libérer un slot."}), 400
    else:
        empty_col = db.find_empty_resource_slot(user_id)
        if empty_col is None:
            return jsonify({"error": "Inventaire plein! Veuillez libérer un slot."}), 400
        
        resource_id = db.create_resource(resource_type, quantity, user_id, empty_col)
        return jsonify({
            "success": True,
            "type": "new_resource",
            "resource": {
                "id": resource_id,
                "type": resource_type,
                "quantity": quantity,
                "max_stack": max_stack,
                "emoji": resource.get_emoji(),
                "name": resource.name,
                "color": resource.get_color(),
                "col": empty_col
            }
        }), 200
