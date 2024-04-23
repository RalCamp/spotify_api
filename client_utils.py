import json
import requests
from response_utils import Response

class Client():
    def __init__(self, name, client_id, client_secret, client_auth_token):
        self.name = name
        self.client_id = client_id
        self.client_secret = client_secret
        self.client_auth_token = client_auth_token

    def read_client_auth_token(self):
        with open(f"app_info/{self.name}.json", 'r') as file:
            read_dict = json.loads(file.read())
        self.client_auth_token = read_dict["client_auth_token"]

    def write_client_auth_token(self):
        with open(f"app_info/{self.name}.json", 'r') as file:
            read_dict = json.loads(file.read())
        read_dict["client_auth_token"] = self.client_auth_token
        write_json = json.dumps(read_dict, indent=4)
        with open(f"app_info/{self.name}.json", 'w') as file:
            file.write(write_json)

    def get_client_auth_token(self):
        payload = {
            "Content-Type": "application/x-www-form-urlencoded", 
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret
            }
        r = requests.post('https://accounts.spotify.com/api/token', data=payload)
        self.client_auth_token = r.json()['access_token']
        self.write_client_auth_token()
        return r.json()
    
    def return_client_auth_token(self):
        self.read_client_auth_token()
        return self.client_auth_token

    def client_token_expired(self):
        self.read_client_auth_token()
        if self.client_auth_token == "":
            self.get_client_auth_token()
            return False
        else:
            hdrs = {
                "Authorization": f"Bearer {self.client_auth_token}"
            }
            r = requests.get("https://api.spotify.com/v1/playlists/3cEYpjA9oz9GiPac4AsH4n", headers=hdrs)
            if r.status_code == 401:
                return True
            elif Response.request_successful(r):
                return False
            else:
                Response.error_message(r)
    