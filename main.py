from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

date = input(
    "Which year do ypu want to travel to? Type the date in this format YYYY-MM-DD: \n")
year = date.split("-")[0]

URL = "https://www.billboard.com/charts/hot-100/2000-08-12/"

SPOTIPY_CLIENT_ID = "e4614f7e587e47e5891d2bec60ee7dd1"
SPOTIPY_CLIENT_SECRET = "272abe6f3e674dd9b980f0b42531ec2d"
SPOTIPY_REDIRECT_URI = "http://my_sptfy_site"

response = requests.get(URL)
website_html = response.text

soup = BeautifulSoup(website_html, "html.parser")

song_names = soup.find_all(name="h3", id="title-of-a-story")
song_names = [song.getText().strip("\n") for song in song_names[3:103]]

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=SPOTIPY_REDIRECT_URI,
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
print(user_id)
song_uris = []

for song in song_names:
    result = sp.search(q=f"track:{song} year: {year}", type="track")
    # print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
    except IndexError:
        pass
    else:
        song_uris.append(uri)

playlist = sp.user_playlist_create(
    user=user_id, name=f"{date} Billboard 100", public=False)
sp.user_playlist_add_tracks(
    user=user_id, playlist_id=playlist["id"], tracks=song_uris)
