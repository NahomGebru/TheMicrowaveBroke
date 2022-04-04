from app import app, db
import random
import os
import requests

import flask
from flask import Flask, render_template, session, request, redirect, abort, jsonify
from flask_login import login_user, current_user, LoginManager, logout_user
from flask_login.utils import login_required
from models import User, Rating

from wikipedia import get_wiki_link
from tmdb import get_movie_data
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")


login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

bp = flask.Blueprint(
    "bp",
    __name__,
    template_folder="./static/react",
)


@bp.route("/new_page")
def new_page():
    return flask.render_template("index.html")


app.register_blueprint(bp)


@login_manager.user_loader
def load_user(user_name):
    return User.query.get(user_name)


@app.route("/get_reviews")
@login_required
def foo():
    ratings = Rating.query.filter_by(username=current_user.username).all()
    return flask.jsonify(
        [
            {
                "rating": rating.rating,
                "comment": rating.comment,
                "movie_id": rating.movie_id,
            }
            for rating in ratings
        ]
    )


@app.route("/save_reviews", methods=["POST"])
def save_reviews():
    data = flask.request.json
    user_ratings = Rating.query.filter_by(username=current_user.username).all()
    new_ratings = [
        Rating(
            username=current_user.username,
            rating=r["rating"],
            comment=r["comment"],
            movie_id=r["movie_id"],
        )
        for r in data
    ]
    for rating in user_ratings:
        db.session.delete(rating)
    for rating in new_ratings:
        db.session.add(rating)
    db.session.commit()
    return flask.jsonify("Ratings successfully saved")


@app.route("/signup")
def signup():
    return flask.render_template("signup.html")


@app.route("/signup", methods=["POST"])
def signup_post():
    username = flask.request.form.get("username")
    user = User.query.filter_by(username=username).first()
    if user:
        pass
    else:
        user = User(username=username)
        db.session.add(user)
        db.session.commit()

    return flask.redirect(flask.url_for("login"))


@app.route("/login")
def login():
    return flask.render_template("login.html")


@app.route("/login", methods=["POST"])
def login_post():
    if request.args.get("next"):
        session["next"] = request.args.get("next")
        return redirect(
            f"https://accounts.google.com/o/oauth2/v2/auth?scope=https://www.googleapis.com/auth/userinfo.profile&access_type=offline&include_granted_scopes=true&response_type=code&redirect_uri=http://127.0.0.1:5000/authorized&client_id={GOOGLE_CLIENT_ID}"
        )
    username = flask.request.form.get("username")
    user = User.query.filter_by(username=username).first()
    if user:
        login_user(user)
        return flask.redirect(flask.url_for("index"))

    else:
        return flask.jsonify({"status": 401, "reason": "Username or Password Error"})


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
    access_token = r.json()["access_token"]
    r = requests.get(
        f"https://www.googleapis.com/oauth2/v2/userinfo?access_token={access_token}"
    ).json()
    return r


MOVIE_IDS = [
    157336,  # actually IDK what this is
]


@app.route("/rate", methods=["POST"])
def rate():
    data = flask.request.form
    rating = data.get("rating")
    comment = data.get("comment")
    movie_id = data.get("movie_id")

    new_rating = Rating(
        username=current_user.username,
        rating=rating,
        comment=comment,
        movie_id=movie_id,
    )

    db.session.add(new_rating)
    db.session.commit()
    return flask.redirect("index")


@app.route("/")
def landing():
    if current_user.is_authenticated:
        return flask.redirect("index")
    return flask.redirect("login")


@app.route("/logout")
def logout():
    logout_user()
    return flask.redirect("login")


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


if __name__ == "__main__":
    app.run(
        host=os.getenv("IP", "0.0.0.0"),
        # port=int(os.getenv("PORT", 8080)),
        debug=True,
    )
