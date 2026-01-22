import os
from flask import Flask
from models import db, bcrypt

def create_app() -> Flask:
    app = Flask(__name__)
    
    base_dir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(base_dir, "rolsa.db")
    
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    db.init_app(app)
    bcrypt.init_app(app)
    
    @app.route("/")
    def home():
        return "Welcome to Rolsa Technologies"
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
    