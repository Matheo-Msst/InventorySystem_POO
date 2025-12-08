from flask import Flask, render_template, abort, request, redirect, url_for
from services.user_service import get_all_users, get_user_by_id
from services.inventory_service import InventoryService
from models.item import Item
from services.database import init_db


inv = InventoryService()
app = Flask(__name__)
items_registry = []
next_item_id = 1 

@app.route("/admin", methods=["GET", "POST"])
def admin():
    global next_item_id 
    users = get_all_users()

    if request.method == "POST":
        item_name = request.form.get("item_name")
        user_id = int(request.form.get("user_id"))

        user = get_user_by_id(user_id)  
        new_item = Item(next_item_id, item_name, user)  

        next_item_id += 1  
        items_registry.append(new_item)

        for c, slot in enumerate(user.inventory[0]):
            if slot == "":
                user.inventory[0][c] = new_item
                new_item.col = c
                break

        return redirect(url_for("admin"))

    return render_template("admin.html", users=users, items=items_registry)

@app.route("/")
def home():
    users = get_all_users()
    return render_template("index.html", users=users)

@app.route("/user/<int:user_id>")
def user_page(user_id):
    user = get_user_by_id(user_id)
    if not user:
        return "Utilisateur introuvable", 404
    
    return render_template("inventoryUser.html", user=user)

def main():
    # 1) Initialiser la base (crée la table si besoin)
    print("🚀 Initialisation de la base de données...")
    init_db()
    print("✅ Base initialisée.\n")



if __name__ == "__main__":
    app.run(debug=True)
