from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(120), nullable=False)
    years = db.Column(db.Integer, nullable=True)
    description = db.Column(db.Text, nullable=False)
    position = db.Column(db.String(120), nullable=True)  # қызметі
    photo = db.Column(db.String(255), nullable=False, default="default.png")
