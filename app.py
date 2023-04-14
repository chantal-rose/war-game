"""Module that contains application entry point."""
from flask import render_template

import config
from models import Win


app = config.connex_app
app.add_api(config.basedir / "swagger.yml")


@app.route("/")
def home():
    players = Win.query.all()
    players.sort(key=lambda x: x.wins, reverse=True)
    return render_template("home.html", players=players)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
    