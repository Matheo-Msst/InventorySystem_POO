from flask import Flask, render_template, request, redirect, url_for
from domaine.inventory import Inventory
from infrastructure.item_factory import get_all_items
from domaine.enchantment import Enchantment, EnchantmentType

app = Flask(__name__)

inventory = Inventory()  # Singleton


@app.route("/")
def index():
    slots = list(enumerate(inventory.slots))
    return render_template("index.html", slots=slots)


@app.route("/add", methods=["GET", "POST"])
def add_item():
    items = get_all_items()

    if request.method == "POST":
        key = request.form["item"]
        quantity = int(request.form.get("quantity", 1))

        item = items[key][1]()  # factory.create()
        inventory.add_item(item, quantity)

        return redirect(url_for("index"))

    return render_template("add_item.html", items=items)


@app.route("/remove", methods=["POST"])
def remove_item():
    name = request.form["name"]
    quantity = int(request.form["quantity"])
    inventory.remove_item(name, quantity)
    return redirect(url_for("index"))

@app.route("/enchant/<int:slot>", methods=["GET", "POST"])
def enchant(slot):
    item = inventory.get_item(slot)

    if item is None or not item.is_equipment():
        return redirect(url_for("index"))

    if request.method == "POST":
        ench_type = EnchantmentType[request.form["enchantment"]]
        level = int(request.form["level"])
        item.add_enchantment(Enchantment(ench_type, level))
        return redirect(url_for("index"))

    return render_template(
        "enchant.html",
        slot=slot,
        item=item,
        enchantments=EnchantmentType
    )

@app.route("/clear")
def clear():
    inventory.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
