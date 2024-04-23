import requests
from app_files.response_utils import Response

class User():
    def __init__(self, userauth):
        self.userauth = userauth

    def get_user_info(self):
        self.userauth.read_user_auth_token()
        if self.userauth.user_auth_token_expired():
            self.userauth.user_auth_token_from_refresh_token()
        hdrs = {
            "Authorization": f"Bearer {self.userauth.return_user_auth_token()}",
            "scope": "user-read-private"
        }
        r = requests.get('https://api.spotify.com/v1/me', headers=hdrs)
        if Response.request_successful(r):
            return r.json()
        else:
            Response.error_message(r)