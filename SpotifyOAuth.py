from http import client
import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
from flask import Flask, render_template_string

app = Flask(__name__)
# Loading environment variables from .env file
load_dotenv()
client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')

scope = "playlist-read-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope=scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri))

@app.route('/')
def index():
# Defining username and playlist ID
    username = input("Enter your Spotify username: ")
    playlist_name = input("Enter playlist name: ")

    results = sp.search(q=playlist_name, type='playlist')

    # Retrieving playlist
    if len(results['playlists']['items']) > 0:
        playlist = results['playlists']['items'][0]
        playlist_id = playlist['id']
        playlist_name = playlist['name']

        playlist = sp.user_playlist(username, playlist_id)

        total_tracks = playlist['tracks']['total']

        print(f"Playlist Name: {playlist_name}")

        tracks = playlist['tracks']['items']
        data = []
        for track in tracks:
            track_name = track['track']['name']
            artists = ", ".join([artist['name'] for artist in track['track']['artists']])
            album_name = track['track']['album']['name']
            data.append({'Track name': track_name, 'Album name': album_name, 'Artists': artists})
        if data:
            df = pd.DataFrame(data)
            df.style.set_properties(**{'border': 'solid green'})
            html_table = df.to_html(index=False)
            return html_table
    else:
        print("Playlist not found")

if __name__ == '__main__':
    app.run(debug=True)
