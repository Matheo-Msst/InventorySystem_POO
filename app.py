from flask import Flask, render_template
from services.user_service import get_all_users, get_user_by_id

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True)
