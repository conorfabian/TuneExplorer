from cs50 import SQL

db = SQL("sqlite:///songs.db")

def recs(song):
    temp = db.execute("SELECT energy FROM songs WHERE song_name = ?", song)
    temp2 = temp[0]['energy']
    energy = str(temp2)[:3]
    temp1 = db.execute("SELECT tempo FROM songs WHERE song_name = ?", song)
    temp2 = temp1[0]['tempo']
    tempo = str(temp2)[:2]
    songs = db.execute("SELECT song_name, artist FROM songs WHERE song_name != ? AND tempo LIKE ? AND energy LIKE ? ORDER BY energy LIMIT 10", song, tempo+"%", energy+"%") #works
    return songs