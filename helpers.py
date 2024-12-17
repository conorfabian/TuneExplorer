from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_recommendations(token, song_name):
    results = search_for_song(token, song_name)
    results = results[0]
    song_id = results["id"]
    audio_features = song_audio_features(token, song_id)
    acousticness = audio_features["acousticness"]
    danceability = audio_features["danceability"]
    energy = audio_features["energy"]
    instrumentalness = audio_features["instrumentalness"]
    liveness = audio_features["liveness"]
    loudness = audio_features["loudness"]
    mode = audio_features["mode"]
    speechiness = audio_features["speechiness"]
    tempo = audio_features["tempo"]
    valence = audio_features["valence"]
    recs = get_recommendations_for_song(token, song_id, acousticness, danceability, energy, instrumentalness, liveness, loudness, mode, speechiness, tempo, valence)
    return recs

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result  = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_song(token, song_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={song_name}&type=track&limit=10"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["tracks"]["items"]
    if len(json_result) == 0:
        print("No song with this name exists...")
        return None
    return json_result

def song_audio_features(token, song_id):
    url = f"https://api.spotify.com/v1/audio-features/{song_id}"
    headers = get_auth_header(token)

    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result

def get_recommendations_for_song(token, song_id, acousticness, danceability, energy, instrumentalness, liveness, loudness, mode, speechiness, tempo, valence):
    url = "https://api.spotify.com/v1/recommendations"
    headers = get_auth_header(token)
    query = f"?limit=51&market=US&seed_tracks={song_id}&target_acousticness={acousticness}&target_danceability={danceability}&target_energy={energy}&target_instrumentalness={instrumentalness}&target_liveness={liveness}&target_loudness={loudness}&target_mode={mode}&target_speechiness={speechiness}&target_tempo={tempo}&target_valence={valence}"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result