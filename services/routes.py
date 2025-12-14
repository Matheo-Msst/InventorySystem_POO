from flask import Blueprint, render_template, abort, request, redirect, url_for, jsonify
from services.user_service import get_all_users, get_user_by_id
from services.inventory_service import InventoryService
from services.chest_service import ChestService
from services.farm_service import FarmService
from services import database as db
from models.item import Item
from models.item_types.armes import Weapon
from models.item_types.rareter import Rareter
from models.item_types.ressource import Resource, RessourceType

inv = InventoryService()
chest_service = ChestService()
farm_service = FarmService()

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

    # Charger les armes
    user_weapons = db.get_user_weapons(user_id)
    # Charger les ressources
    user_resources = db.get_user_resources(user_id)
    
    inventory = [""] * 9
    
    # Placer les armes EN PREMIER
    for weapon_row in user_weapons:
        if weapon_row['col'] is not None and 0 <= weapon_row['col'] < 9:
            try:
                rarity = Rareter[weapon_row['rarity']]
            except KeyError:
                rarity = Rareter.COMMUN
            
            weapon = Weapon(weapon_row['id'], weapon_row['name'], rarity)
            inventory[weapon_row['col']] = weapon
    
    # Placer les ressources ENSUITE (sans écraser les armes)
    for resource_row in user_resources:
        try:
            resource_type = RessourceType[resource_row['resource_type']]
        except KeyError:
            continue
        
        resource = Resource(
            resource_row['id'],
            resource_type,
            resource_row['quantity']
        )
        
        # Si le slot de la ressource est vide, l'utiliser
        if resource_row['col'] is not None and 0 <= resource_row['col'] < 9:
            if inventory[resource_row['col']] == "":
                inventory[resource_row['col']] = resource
            else:
                # Sinon, chercher le premier slot vide
                placed = False
                for i in range(9):
                    if inventory[i] == "":
                        inventory[i] = resource
                        # Mettre à jour la BD avec le nouveau col
                        db.update_resource(resource_row['id'], col=i)
                        placed = True
                        break
                if not placed:
                    # Si aucun slot vide, ne pas ajouter (inventaire plein)
                    pass
        else:
            # Si pas de col, chercher le premier slot vide
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


@routes_bp.route("/farm/<int:user_id>")
def farm_page(user_id):
    """Affiche la page du farming"""
    user = get_user_by_id(user_id)
    if not user:
        return "Utilisateur introuvable", 404
    
    farming_info = farm_service.get_farming_info()
    return render_template("farm.html", user=user, farming_info=farming_info)


@routes_bp.route("/api/farm/<int:user_id>", methods=["POST"])
def farm_resource(user_id):
    """API: Farm une ressource aléatoire"""
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "Utilisateur introuvable"}), 404
    
    # Générer une ressource aléatoire
    resource = farm_service.generate_random_resource()
    resource_type = resource.resource_type.name
    quantity = resource.quantity
    max_stack = resource.get_max_stack()
    
    # Essayer de stacker avec une ressource existante
    stackable_col, stackable_id, current_qty = db.find_stackable_resource_slot(user_id, resource_type)
    
    if stackable_col is not None:
        # On peut stacker dans un slot existant
        new_quantity = current_qty + quantity
        
        if new_quantity <= max_stack:
            # Tout rentre dans le stack existant
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
            # Le stack déborde
            overflow = new_quantity - max_stack
            db.update_resource(stackable_id, quantity=max_stack)
            
            # Placer le débordement dans un nouveau slot
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
        # Créer une nouvelle ressource dans un slot vide
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
