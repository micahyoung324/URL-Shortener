from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import string
import random

SHORT_LENGTH = 4

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///urls.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Urls(db.Model):
    id_ = db.Column("id_", db.Integer, primary_key=True)
    long = db.Column("long", db.String())
    short = db.Column("short", db.String(SHORT_LENGTH))

    def __init__(self, long, short):
        self.long = long
        self.short = short

def shorten_url():
    letters = string.ascii_letters

    while True:
        random_letters = random.choices(letters, k=SHORT_LENGTH)
        random_letters = "".join(random_letters)

        short_url = Urls.query.filter_by(short=random_letters).first()

        if not short_url:
            return random_letters

@app.before_first_request
def create_tables():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        url_received = request.form["nm"]

        # Check if URL already exists in the db
        found_url = Urls.query.filter_by(long=url_received).first()

        if found_url:
            # URL found so just turn short URL
            return redirect(url_for("display_short_url", url=found_url.short))

        else:
            # URL not found so we need to create a short URL
            short_url = shorten_url()
            new_url = Urls(url_received, short_url)
            db.session.add(new_url)
            db.session.commit()
            return redirect(url_for("display_short_url", url=short_url))

        return url_received
    else:
        return render_template("home.html")

@app.route("/display/<url>")
def display_short_url(url):
    return render_template("shorturl.html", short_url_display=url)

@app.route("/<short_url>")
def redirection(short_url):
    long_url = Urls.query.filter_by(short=short_url).first()
    if long_url:
        return redirect(long_url.long)
    else:
        return render_template("nourl.html")

if __name__ == "__main__":
    app.run(port = 5000, debug = True)
