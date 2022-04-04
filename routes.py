from logging import Filter
from app import app, db
import random
import os

import flask
from flask_login import login_user, current_user, LoginManager, logout_user
from flask_login.utils import login_required
from models import Filters, Ingredients, User, Rating

from wikipedia import get_wiki_link
from tmdb import get_movie_data

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



@app.route("/get_userinfo")
@login_required
def userinfo():
    userInfos = User.query.filter_by(username=current_user.username).all()
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
def foo():
    ingredients = Ingredients.query.filter_by(username=current_user.username).all()
    return flask.jsonify(
        [
            {
                "Ingredients": ingredient.ingredients,

            }
            for ingredient in ingredients
        ]
    )


@app.route("/get_filter")
@login_required
def get_filter():
    userFilters = Filters.query.filter_by(username=current_user.username).all()
    return flask.jsonify(
        [
            {
                "cuisineFilter": f.cuisineFilter,
                "allergyFilter": f.allergyFilter,
                "dietFilter": f.dietFilter,

            }
            for f in userFilters
        ]
    )

@app.route("/save_ingredients", methods=["POST"])
def save_ingredients():
    data = flask.request.json
    user_ingredients = Ingredients.query.filter_by(username=current_user.username).all()
    new_ingredients = [
        Ingredients(
            username=current_user.username,
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
    user_filters = Filters.query.filter_by(username=current_user.username).all()
    new_filters = [
        Filters(
            username=current_user.username,
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



@app.route("/save_info", methods=["POST"])
def save_info():
    data = flask.request.json
    user_info = User.query.filter_by(username=current_user.username).all()
    new_info = [
        User(
            username=current_user.username,
            actualName=r["actualName"],
            address=r["address"],
            bio=r["bio"]
        )
        for r in data
    ]
    for info in user_info:
        db.session.delete(info)
    for info in new_info:
        db.session.add(info)
    db.session.commit()
    return flask.jsonify("User infrormation successfully saved")


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
    username = flask.request.form.get("username")
    user = User.query.filter_by(username=username).first()
    if user:
        login_user(user)
        return flask.redirect(flask.url_for("index"))

    else:
        return flask.jsonify({"status": 401, "reason": "Username or Password Error"})


MOVIE_IDS = [
    157336,  # actually IDK what this is
]


@app.route("/ingredient_list", methods=["POST"])
def ingredient_list():
    data = flask.request.form
    ingredients = data.get("ingredients")


    new_ingredient = Ingredients(
        username=current_user.username,
        ingredients=ingredients,
    )

    db.session.add(new_ingredient)
    db.session.commit()
    return flask.redirect("index")


@app.route("/user_list", methods=["POST"])
def user_list():
    data = flask.request.form
    actualName = data.get("actualName")
    address = data.get("address")
    bio = data.get("bio")

    new_user = User(
        username=current_user.username,
        actualName=actualName,
        address= address,
        bio=bio,
    )

    db.session.add(new_user)
    db.session.commit()
    return flask.redirect("index")


@app.route("/filter_list", methods=["POST"])
def filter_list():
    data = flask.request.form
    cuisineFilter = data.get("cuisineFilter")
    allergyFilter = data.get("allergyFilter")
    dietFilter = data.get("dietFilter")

    new_filter = Filters(
        username=current_user.username,
        cuisineFilter=cuisineFilter,
        allergyFilter= allergyFilter,
       dietFilter=dietFilter,
    )

    db.session.add(new_filter)
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
