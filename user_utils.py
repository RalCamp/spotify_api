import requests
import json
from response_utils import Response

class User():
    def __init__(self, user_auth_token, user_refresh_token):
        self.user_auth_token = user_auth_token
        self.user_refresh_token = user_refresh_token

    def read_user_auth_token(self):
        with open(f"app_info/{self.name}.json", 'r') as file:
            read_dict = json.loads(file.read())
        self.user_auth_token = read_dict["user_auth_token"]

    def get_user_info(self, user_auth_token):
        self.read_user_auth_token(user_auth_token)
        if self.user_auth_token_expired(user_auth_token):
            self.user_auth_token_from_refresh_token(user_auth_token)
        hdrs = {
            "Authorization": f"Bearer {user_auth_token}",
            "scope": "user-read-private"
        }
        r = requests.get('https://api.spotify.com/v1/me', headers=hdrs)
        if Response.request_successful(r):
            return r.json()
        else:
            Response.error_message(r)