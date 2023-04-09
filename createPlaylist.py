import os
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import time


load_dotenv()
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SECRET = os.getenv('SPOTIFY_CLIENT_SECRT')
GRASPOP_BAND_URL = os.getenv('GRASPOP_BAND_LIST')
REDIRECT_URI = os.getenv('REDIRECT_URI')
SCOPE = os.getenv('SCOPE')
USERNAME = os.getenv('USERNAME')
playlist_name = 'Graspop 2023'


def generate_lists_of_songs(sp, artist):
    results = sp.search(q='artist:' + artist, type='artist')
    artist = results['artists']['items'][0]
    artist_uri = artist['uri']
    recommendations = sp.artist_top_tracks(artist_uri)
    track_list = recommendations['tracks']
    list_of_songs = []
    for tracks in track_list:
        # print(tracks['name'])
        list_of_songs.append(tracks['uri'])
    return list_of_songs


def create_spotify():
    token = SpotifyOAuth(client_id=CLIENT_ID, client_secret=SECRET,
                         redirect_uri=REDIRECT_URI, scope=SCOPE, username=USERNAME)
    sp = spotipy.Spotify(auth_manager=token)
    return token, sp


response = requests.get(GRASPOP_BAND_URL)

# Parse the HTML content using Beautiful Soup
soup = BeautifulSoup(response.content, 'html.parser')

# Extract all the data from the selector
artists_list = []
for item in soup.select(".artist__name"):
    artists_list.append(item.text)

# Print the extracted data


token, sp = create_spotify()
playlist = sp.user_playlists(sp.me()["id"])['items'][0]['name']
if (playlist != playlist_name):
    sp.user_playlist_create(
        user=sp.me()["id"], name=playlist_name, public=True)
prePlaylists = sp.user_playlists(user=sp.me()["id"])
playlist = prePlaylists['items'][0]['id']
for artist in artists_list:
    print(artist)
    list_of_songs = generate_lists_of_songs(sp, artist)
    token.get_cached_token()
    token_info = token.cache_handler.get_cached_token()
    if token.is_token_expired(token_info):
        token, sp = create_spotify()
    sp.user_playlist_add_tracks(
        user=sp.me()["id"], playlist_id=playlist, tracks=list_of_songs)
print('done')
