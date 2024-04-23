import requests
from response_utils import Response

class Track():
    def __init__(self, client):
        self.client = client

    def get_track_info(self, track_id):
        self.client.read_client_auth_token()
        if self.client.client_token_expired():
            self.client.get_client_auth_token()
        hdrs = {
            "Authorization": f"Bearer {self.client.return_client_auth_token()}"
        }
        r = requests.get(f"https://api.spotify.com/v1/tracks/{track_id}", headers=hdrs)
        if Response.request_successful(r):
            return r.json()
        else:
            Response.error_message(r)