from flask import Flask
from services.routes import routes_bp
from services.database import init_db

app = Flask(__name__)

app.register_blueprint(routes_bp)

def main():
    init_db()


if __name__ == "__main__":
    main()
    app.run(debug=True)
