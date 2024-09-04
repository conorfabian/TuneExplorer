from flask import Flask, redirect, render_template, request, session
from cs50 import SQL
from flask_session import Session

from helpers import recs

db = SQL("sqlite:///songs.db")

app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        song = request.form.get("song-input")
        name = db.execute("SELECT song_name FROM songs WHERE song_name LIKE ?", song) # not able to user LIKE here because for some reason the % is being put in outside the '' which is causing the error

        if not name:
            return render_template("not_found.html")

        session['song'] = song
        return redirect("/recommend")

    else:
        return render_template("index.html")

@app.route("/recommend", methods=["GET"])
def recommend():
    song_name = session['song']
    temp = db.execute("SELECT artist FROM songs WHERE song_name = ?", song_name)
    artist = temp[0]['artist']
    recommendations = recs(song_name)
    return render_template("recommend.html", name=song_name, artist=artist, recs=recommendations)