# app/models.py
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize SQLAlchemy
db = SQLAlchemy()

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    address = db.Column(db.String(150))
    email = db.Column(db.String(50), unique=True)
    mobile = db.Column(db.String(20))
    password = db.Column(db.String(200))  # Store hashed password


