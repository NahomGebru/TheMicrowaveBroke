# pylint: disable=import-error
import flask
import os
from flask_sqlalchemy import SQLAlchemy 
from dotenv import find_dotenv, load_dotenv  

load_dotenv(find_dotenv())

app = flask.Flask(__name__)
# Point SQLAlchemy to your Heroku database
db_url = os.getenv("DATABASE_URL")
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
# Gets rid of a warning
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
