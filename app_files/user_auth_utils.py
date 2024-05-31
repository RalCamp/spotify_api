import requests
import json
import base64
from app_files.response_utils import Response

class UserAuth():
    def __init__(self, app_name, user_auth_token, user_refresh_token, client_id, client_secret):
        self.app_name = app_name
        self.user_auth_token = user_auth_token
        self.user_refresh_token = user_refresh_token
        self.client_id = client_id
        self.client_secret = client_secret

    def read_user_auth_token(self):
        with open(f"app_files/app_info/{self.app_name}.json", 'r') as file:
            read_dict = json.loads(file.read())
        self.user_auth_token = read_dict["user_auth_token"]

    def read_user_refresh_token(self):
        with open(f"app_files/app_info/{self.app_name}.json", 'r') as file:
            read_dict = json.loads(file.read())
        self.user_refresh_token = read_dict["user_refresh_token"]

    def write_user_auth_token(self):
        with open(f"app_files/app_info/{self.app_name}.json", 'r') as file:
            read_dict = json.loads(file.read())    
        read_dict["user_auth_token"] = self.user_auth_token
        write_json = json.dumps(read_dict, indent=4)
        with open(f"app_files/app_info/{self.app_name}.json", 'w') as file:
            file.write(write_json)

    def write_user_refresh_token(self):
        with open(f"app_files/app_info/{self.app_name}.json", 'r') as file:
            read_dict = json.loads(file.read())    
        read_dict["user_refresh_token"] = self.user_refresh_token
        write_json = json.dumps(read_dict, indent=4)
        with open(f"app_files/app_info/{self.app_name}.json", 'w') as file:
            file.write(write_json)

    def return_user_auth_token(self):
        self.read_user_auth_token()
        return self.user_auth_token

    def user_auth_token_expired(self):
        self.read_user_auth_token()
        hdrs = {
            "Authorization": f"Bearer {self.user_auth_token}",
            "scope": "user-read-private"
        }
        r = requests.get('https://api.spotify.com/v1/me', headers=hdrs)
        if r.status_code == 401:
            return True
        elif Response.request_successful(r):
            return False
        else:
            Response.error_message(r)
        
    def get_user_refresh_token(self):
        encoded_credentials = base64.b64encode(self.client_id.encode() + b':' + self.client_secret.encode()).decode("utf-8")
        prms = {
            "grant_type": "refresh_token",
            "refresh_token": self.user_refresh_token
        }
        hdrs = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": encoded_credentials
        }
        r = requests.post("https://accounts.spotify.com/api/token", params=prms, headers=hdrs)
        if Response.request_successful(r):
            self.user_refresh_token = r.json()['refresh_token']
            self.write_user_refresh_token()
            return r.json()
        else:
            Response.error_message()

    def user_auth_token_from_refresh_token(self):
        self.read_user_refresh_token()
        encoded_credentials = base64.b64encode(self.client_id.encode() + b':' + self.client_secret.encode()).decode("utf-8")
        token_headers = {
            "Authorization": "Basic " + encoded_credentials,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        token_params = {
            "grant_type": "refresh_token",
            "refresh_token": self.user_refresh_token
        }
        r = requests.post("https://accounts.spotify.com/api/token", params=token_params, headers=token_headers)
        if Response.request_successful(r):
            self.user_auth_token = r.json()["access_token"]
            self.write_user_auth_token()
            print("User authorisation token acquired\n")
            return r.json()
        else:
            Response.error_message(r)

    def manage_userauth_creds(self):
        self.return_user_auth_token()
        if self.user_auth_token_expired():
            print("The current user authorisation token has expired")
            print("Requesting a new token...")
            self.user_auth_token_from_refresh_token()