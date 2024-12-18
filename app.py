from flask import Flask, redirect, render_template, request, session

from helpers import get_token, get_recommendations, search_for_song

app = Flask(__name__)
app.secret_key = "TuneExplorer"


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        song = request.form.get("song-input")
        session['song'] = song # session not working as well
        # return redirect("/get_song") - not done here, need to add route into which user selects from different songs that pop up when searched and then they choose the correct one
        return redirect("/find")

    else:
        return render_template("index.html") # also need to work on html more to make it look like a brand - PutEmOn or whatever
    

@app.route("/find", methods=["GET", "POST"])
def find():
    if request.method == "POST":
        song_name = request.form.get("song") #not working correctly, only selecting first song from options
        session['song'] = song_name
        return redirect("/recommend")
    else:
        song_name = session['song']
        token = get_token()
        results = search_for_song(token, song_name)
        return render_template("find.html", results=results, name=song_name)


@app.route("/recommend", methods=["GET"])
def recommend():
    song_name = session['song']
    token = get_token()
    results = search_for_song(token, song_name)
    results = results[0]
    name = results["name"]
    artist = results["artists"][0]["name"]
    recs = get_recommendations(token, song_name)
    for song in recs:
        if song["name"] == results["name"] and song["artists"][0]["name"] == results["artists"][0]["name"]:
            recs.remove(song)
    return render_template("recommend.html", name=name, artist=artist, recs=recs)


if __name__ == "__main__":
    app.debug = False
    app.run()
