from flask import Flask, render_template
from controllers.user_controller import get_users

app = Flask(__name__)

@app.route("/")
def home():
    users = get_users()  # Appel à la couche contrôleur
    return render_template("index.html", users=users)

if __name__ == "__main__":
    app.run(debug=True)
