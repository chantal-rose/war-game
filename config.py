"""Module that gets the necessary modules imported into the program and configured, including the creation of the database."""
import pathlib

import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

basedir = pathlib.Path(__file__).parent.resolve()
connex_app = connexion.App(__name__, specification_dir=basedir)

app = connex_app.app
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{basedir / 'db/wins.db'}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


@app.before_first_request
def create_tables():  # pragma: no cover
    db.create_all()


db = SQLAlchemy(app)
ma = Marshmallow(app)
