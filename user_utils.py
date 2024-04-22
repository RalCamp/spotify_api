import requests
from response_utils import Response
from user_auth_utils import UserAuth

class User():
    def __init__(self, name, user_auth_token, user_refresh_token, client_id, client_secret):
        self.name = name
        self.user_auth_token = user_auth_token
        self.user_refresh_token = user_refresh_token
        self.client_id = client_id
        self.client_secret = client_secret
        self.UserAuth = UserAuth(self.name, self.user_auth_token, self.user_refresh_token, self.client_id, self.client_secret)

    def get_user_info(self):
        self.UserAuth.read_user_auth_token()
        if self.UserAuth.user_auth_token_expired():
            self.UserAuth.user_auth_token_from_refresh_token()
        hdrs = {
            "Authorization": f"Bearer {self.user_auth_token}",
            "scope": "user-read-private"
        }
        r = requests.get('https://api.spotify.com/v1/me', headers=hdrs)
        if Response.request_successful(r):
            return r.json()
        else:
            Response.error_message(r)