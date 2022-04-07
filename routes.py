from crypt import methods
from pickle import GET
from app import app, db
import os
import requests

import flask
from flask import Flask, render_template, session, request, redirect, abort, jsonify
from flask_login.utils import login_required
from Userfetch import login_required
from models import Ingredients, User, Filters
from termcolor import colored
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")


bp = flask.Blueprint(
    "bp",
    __name__,
    template_folder="./static/react",
)


@bp.route("/new_page")
def new_page():
    return flask.render_template("index.html")


app.register_blueprint(bp)


@app.route("/login")
def login():
    if request.args.get("next"):
        session["next"] = request.args.get("next")
        return redirect(
            f"https://accounts.google.com/o/oauth2/v2/auth?scope=https://www.googleapis.com/auth/userinfo.profile&access_type=offline&include_granted_scopes=true&response_type=code&redirect_uri=http://127.0.0.1:5000/authorized&client_id={GOOGLE_CLIENT_ID}"
        )
    return render_template("login.html")


@app.route("/authorized")
def google_authorized():
    r = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "code": request.args.get("code"),
            "grant_type": "authorization_code",
            "redirect_uri": "http://127.0.0.1:5000/authorized",
        },
    )
    print(colored(r.json(), "red"))
    r = requests.get(
        f'https://www.googleapis.com/oauth2/v2/userinfo?access_token={r.json()["access_token"]}'
    ).json()
    user = User.query.filter_by(googleId=str(r["id"])).all()
    print(user)
    print(user[0])
    if len(user) != 0:
        session["user_id"] = user[0].googleId
        session["name"] = user[0].actualName
    else:
        google_id = str(r["id"])
        google_name = r["name"]

        new_user = User(
            googleId=google_id,
            actualName=google_name,
        )

        db.session.add(new_user)
        db.session.commit()

    if session.get("next"):
        return redirect(session.get("next"))
    return redirect("/")


@app.route("/get_userinfo")
@login_required
def userinfo():
    userInfos = User.query.filter_by(googleId=session["user_id"]).all()
    return flask.jsonify(
        [
            {
                "actualName": info.actualName,
                "address": info.address,
                "bio": info.bio,
            }
            for info in userInfos
        ]
    )


@app.route("/get_ingredients")
@login_required
def getIngredients():
    ingredients = Ingredients.query.filter_by(googleId=session["user_id"]).all()
    return flask.jsonify(
        [{"Ingredients": ingredient.ingredients} for ingredient in ingredients]
    )


@app.route("/get_filter")
@login_required
def getFilter():
    userFilters = Ingredients.query.filter_by(googleId=session["user_id"]).all()
    return flask.jsonify(
        [
            {
                "cuisineFilter": filter.cuisineFilter,
                "allergyFilter": filter.allergyFilter,
                "dietFilter": filter.dietFilter,
            }
            for filter in userFilters
        ]
    )


@app.route("/save_ingredients", methods=["POST"])
def save_ingredients():
    data = flask.request.json
    user_ingredients = Ingredients.query.filter_by(googleId=session["user_id"]).all()
    new_ingredients = [
        Ingredients(
            googleId=session["user_id"],
            ingredients=r["ingredients"],
        )
        for r in data
    ]
    for ingredients in user_ingredients:
        db.session.delete(ingredients)
    for ingredients in new_ingredients:
        db.session.add(ingredients)
    db.session.commit()
    return flask.jsonify("Ingredients successfully saved")


@app.route("/save_filters", methods=["POST"])
def save_filters():
    data = flask.request.json
    user_filters = Filters.query.filter_by(googleId=session["user_id"]).all()
    new_filters = [
        Filters(
            googleId=session["user_id"],
            cuisineFilter=r["cuisineFilter"],
            allergyFilter=r["cuisineFilter"],
            dietFilter=r["dietFilter"],
        )
        for r in data
    ]
    for fil in user_filters:
        db.session.delete(fil)
    for fil in new_filters:
        db.session.add(fil)
    db.session.commit()
    return flask.jsonify("Filters successfully saved")


@app.route("/ingredient_list", methods=["POST"])
def ingredient_list():
    data = flask.request.form
    ingredients = data.get("ingredients")

    new_ingredient = Ingredients(
        googleId=session["user_id"],
        ingredients=ingredients,
    )

    db.session.add(new_ingredient)
    db.session.commit()
    return flask.redirect("index")


@app.route("/filter_list", methods=["POST"])
def filter_list():
    data = flask.request.form
    cuisineFilter = data.get("cuisineFilter")
    allergyFilter = data.get("allergyFilter")
    dietFilter = data.get("dietFilter")

    new_filter = Filters(
        googleId=session["user_id"],
        cuisineFilter=cuisineFilter,
        allergyFilter=allergyFilter,
        dietFilter=dietFilter,
    )

    db.session.add(new_filter)
    db.session.commit()
    return flask.redirect("index")


@app.route("/")
@login_required
def index():
    return "Success"


@app.route("/logout")
def logout():
    session.clear()
    return flask.redirect("/login")


"""
@app.route("/index")
@login_required
def index():
    movie_id = random.choice(MOVIE_IDS)

    # API calls
    (title, tagline, genre, poster_image) = get_movie_data(movie_id)
    wikipedia_url = get_wiki_link(title)

    ratings = Rating.query.filter_by(movie_id=movie_id).all()

    return flask.render_template(
        "main.html",
        title=title,
        tagline=tagline,
        genre=genre,
        poster_image=poster_image,
        wiki_url=wikipedia_url,
        ratings=ratings,
        movie_id=movie_id,
    )
"""


if __name__ == "__main__":
    app.run(
        debug=True,
    )
