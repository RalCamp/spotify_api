import requests
from response_utils import Response
from client_utils import Client

class Track():
    def __init__(self, name, client_id, client_secret, client_auth_token):
        self.name = name
        self.client_id = client_id
        self.client_secret = client_secret
        self.client_auth_token = client_auth_token
        self.Client = Client(name, self.client_id, self.client_secret, self.client_auth_token)

    def get_track_info(self, track_id):
        self.Client.read_client_auth_token()
        if self.Client.client_token_expired():
            self.Client.get_client_auth_token()
        hdrs = {
            "Authorization": f"Bearer {self.client_auth_token}"
        }
        r = requests.get(f"https://api.spotify.com/v1/tracks/{track_id}", headers=hdrs)
        if Response.request_successful(r):
            return r.json()
        else:
            Response.error_message(r)