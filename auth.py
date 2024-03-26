import requests
from urllib.parse import urlencode
import webbrowser

auth_headers = {
    "client_id": "66768cc0e0fb4cc5a9ae5421aa6c399c",
    "response_type": "code",
    "redirect_uri": "http://localhost:7777/callback",
    "scope": "user-library-read playlist-read-private playlist-modify-private playlist-modify-public",
    "Accept-Encoding": "identity"
}

webbrowser.open("https://accounts.spotify.com/authorize?" + urlencode(auth_headers))