# pylint: disable=import-error
"""
Create Database Tables 
"""
from app import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.BigInteger, primary_key=True)
    googleId = db.Column(db.String(200))
    actualName = db.Column(db.String(800))
    address = db.Column(db.String(80))
    bio = db.Column(db.String(800))


class Ingredients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    googleId = db.Column(db.String(200))
    ingredients = db.Column(db.String(300))


class Filters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    googleId = db.Column(db.String(200))
    cuisineFilter = db.Column(db.String(300))
    allergyFilter = db.Column(db.String(300))
    dietFilter = db.Column(db.String(300))


class Recipes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    googleId = db.Column(db.String(200))
    imageTitle = db.Column(db.String(300))
    recipeLink = db.Column(db.String(300))

db.create_all()