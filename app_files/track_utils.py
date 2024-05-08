import requests
from app_files.response_utils import Response

class Track():
    def __init__(self, client, userauth):
        self.client = client
        self.userauth = userauth

    def manage_client_creds(self):
        self.client.read_client_auth_token()
        if self.client.client_token_expired():
            self.client.get_client_auth_token()

    def manage_userauth_creds(self):
        self.userauth.read_user_auth_token
        if self.userauth.user_auth_token_expired():
            self.userauth.user_auth_token_from_refresh_token()

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

    def get_recommendations(self, limit=20, market=None, seeds={ 'seed_artists': [], 'seed_genres': [], 'seed_tracks': [] }, audio_features=None):
        if seeds['seed_artists'] == [] and seeds['seed_genres'] and seeds['seed_tracks']:
            print("################################################")
            print("ERROR - you must provide at least one of either:\n- seed_artists\n- seed_genres\n- seed_tracks")
            print("################################################")
            return
        url = "https://api.spotify.com/v1/recommendations?"
        if limit != 20:
            url += f"limit={limit}&"
        if market != None:
            url += f"market={market}&"
        for seed in seeds.keys():
            if seeds[seed] != []:
                seed_formatted = '%2C'.join(seeds[seed])
                url += f"{seed}={seed_formatted}&"
        if audio_features != None:
            for feature in audio_features.keys():
                url += f"{feature}={audio_features[feature]}&"
        if url[-1] == "&":
            url = url[0:(len(url)-1)]
        self.manage_userauth_creds()
        hdrs = {
            "Authorization": f"Bearer {self.userauth.return_user_auth_token()}"
        }
        r = requests.get(url, headers=hdrs)
        if Response.request_successful(r):
            return r.json()
        else:
            Response.error_message(r)
