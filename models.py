from datetime import datetime, date, time
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    #store hashed password only (never plaintext)
    password_hash = db.Column(db.String(255), nullable=False)
    # Role can be customer or admin 
    role = db.Column(db.String(20), nullable=False, default="customer")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    # Relationships
    bookings = db.relationship("Booking", backref="user", lazy=True, cascade="all, delete-orphan")
    carbon_calulations = db.relationship("CarbonCalculation", backref="user", lazy=True, cascade="all, delete-orphan")
    energy_usage_records = db.relationship("EnergyUsageRecord", backref="user", lazy=True, cascade="all, delete-orphan")
    accessibility_settings = db.relationship(
        "AccessibilitySettings",
        backref="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
    
    admin_profile = db.relationship(
        "Admin",
        backref="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
    
    # Helper methods would be used in v1.2
    def set_password(self, raw_password: str) -> None:
        self.password_hash = bcrypt.generate_password_hash(raw_password).decode("utf-8")
        
    def check_password(self, raw_password:str ) -> bool:
        return bcrypt.check_password_hash(self.password_hash, raw_password)
    
class Admin(db.Model):
    __tablename__ = "admins"
    id = db.Column(db.Integer, primary_key=True)
    # each admin would map to exactly one user
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    # admin level from staff, manager or superadmin
    admin_level = db.Column(db.String(30), nullable=False, default="staff")
    # optional: store permission as a string for now
    permissions = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
class Booking(db.Model):
    __tablename__ = "bookings"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, primary_key=True)
    # consultation or Installation
    booking_type = db.Column(db.String(50), nullable=False)
    # service category: solar/ev/smart_home
    service_type = db.Column(db.String(30), nullable=False)
    preferred_date = db.Column(db.Date, nullable=False)
    preferred_time = db.Column(db.Time, nullable=False)
    # where installation/consultation happens
    address_line1 = db.Column(db.String(120), nullable=True)
    address_line2 = db.Column(db.String(120), nullable=True)
    city = db.Column(db.String(60), nullable=True)
    postcode = db.Column(db.String(12), nullable=True)
    # pending / confirmed / completed / cancelled
    status = db.Column(db.String(20), nullable=False, default="pending")
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
class CarbonCalculation(db.Model):
    __tablename__ = "carbon_calulations"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    # users inputs and it so we can show history
    electricity_kwh = db.Column(db.Float, nullable=True)
    gas_kwh = db.Column(db.Float, nullable=True)
    petrol_car_miles = db.Column(db.Float, nullable=True)
    ev_miles = db.Column(db.Float, nullable=True)
    #optional period for calulation for weekly/ monthly
    period_start = db.Column(db.Date, nullable=True)
    period_end = db.Column(db.Date, nullable=True)
    # output results
    co2_kg = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
class EnergyUsageRecord(db.Model):
    # for tracking energy usage over time, can also be used of making charts later using matplotlib
    __tablename__ = "energy_usage_records"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    record_date = db.Column(db.Date, nullable=False, default=date.today)
    electricity_kwh = db.Column(db.Float, nullable=True)
    gas_kwh = db.Column(db.Float, nullable=True)
    # optional but for solar generation if users have solar panels it would help with ROI/footprint views
    solar_generation_kwh = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
class AccessibilitySettings(db.Model):
    __tablename__ = "accessibility_settings"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    # langguage support - English/French/Spanish
    language = db.Column(db.String(10), nullable=False, default="en") # en, fr, es
    # Accessibility toogles
    high_contrast = db.Column(db.Boolean, nullable=False, default=False)
    reduced_motion = db.Column(db.Boolean, nullable=False, default=False)
    # font scaling: 1.0 = normal, 1.1 = large, 1.2 = extra large etc.
    font_scale = db.Column(db.Float, nullable=False, default=1.0)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
         
    