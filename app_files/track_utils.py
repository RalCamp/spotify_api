import requests
from app_files.response_utils import Response

class Track():
    def __init__(self, client):
        self.client = client

    def manage_client_creds(self):
        self.client.read_client_auth_token()
        if self.client.client_token_expired():
            self.client.get_client_auth_token()

    def get_track_info(self, track_id):
        self.manage_client_creds()
        hdrs = {
            "Authorization": f"Bearer {self.client.return_client_auth_token()}"
        }
        r = requests.get(f"https://api.spotify.com/v1/tracks/{track_id}", headers=hdrs)
        if Response.request_successful(r):
            return r.json()
        else:
            Response.error_message(r)

    def get_audio_features(self, track_id):
        self.manage_client_creds()
        hdrs = {
            "Authorization": f"Bearer {self.client.return_client_auth_token()}"
        }
        r = requests.get(f"https://api.spotify.com/v1/audio-features/{track_id}", headers=hdrs)
        if Response.request_successful(r):
            return r.json()
        else:
            Response.error_message(r)

    def get_audio_analysis(self, track_id):
        self.manage_client_creds()
        hdrs = {
            "Authorization": f"Bearer {self.client.return_client_auth_token()}"
        }
        r = requests.get(f"https://api.spotify.com/v1/audio-analysis/{track_id}", headers=hdrs)
        if Response.request_successful(r):
            return r.json()
        else:
            Response.error_message(r)