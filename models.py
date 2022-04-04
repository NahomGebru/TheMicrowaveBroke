from app import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    actualName =  db.Column(db.String(80))
    address = db.Column(db.String(80))
    bio  = db.Column(db.String(800))


class Ingredients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    ingredients = db.Column(db.String(300))


class Filters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    cuisineFilter = db.Column(db.String(300))
    allergyFilter = db.Column(db.String(300))
    dietFilter = db.Column(db.String(300))


db.create_all()