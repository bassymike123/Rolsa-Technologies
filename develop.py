import os
from flask import Flask
from models import db, bcrypt # bcrypt is imported to initialise it with the app
from models import User, Admin, Booking, CarbonCalculation, EnergyUsageRecord, AccessibilitySettings

def create_app() -> Flask:
    app = Flask(__name__)
    #db file location, this would create a local sqlite file in my projects folder
    base_dir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(base_dir, "rolsa.db")
    
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    # initialising extensions
    db.init_app(app)
    bcrypt.init_app(app)
    return app


        
if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.drop_all() # For development only this rests the shcema with each run
        db.create_all()
        print("Database successfully created!")
    