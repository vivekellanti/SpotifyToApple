from http import client
import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Loading environment variables from .env file
load_dotenv()
client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')

scope = "playlist-read-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope=scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri))

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

    for track in tracks:
        track_name = track['track']['name']
        artists = track['track']['artists']
        artist_names = ",".join([artist['name'] for artist in artists])
        print(f"{track_name} - {artist_names}")
else:
    print("Playlist not found")
