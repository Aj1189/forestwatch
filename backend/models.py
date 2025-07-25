from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    region = db.Column(db.String(100))
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default='citizen')  # 'citizen' or 'forest_dept'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Project model
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    region = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    trees_target = db.Column(db.Integer, nullable=False)
    trees_planted = db.Column(db.Integer, nullable=False)

# Complaint model
class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    complaint_id = db.Column(db.String(50), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(150), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), default='Open')
    rejection_reason = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('complaints', lazy=True))
