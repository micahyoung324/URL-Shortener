from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///urls.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Urls(db.Model):
    id_ = db.Column("id_", db.Integer, primary_key=True)
    long = db.Column("long", db.String())
    short = db.Column("short", db.String(4))

    def __init__(self, long, short):
        self.long = long
        self.short = short

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
            return redirect(url_for("display_short_url", url = found_url.short))

        else:
            # URL not found so we need to create a short URL
            short_url = shorten_url()
            new_url = Urls(url_received, short_url)
            db.session.add(new_url)
            db.session.commit()
            return short_url

        return url_received
    else:
        return render_template("home.html")

if __name__ == "__main__":
    app.run(port = 5000, debug = True)
