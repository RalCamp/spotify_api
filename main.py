import json
import os

from client_utils import Client
from user_auth_utils import UserAuth
from user_utils import User
from track_utils import Track
from playlist_utils import Playlist
from custom_utils import Custom

class SpotifyApp():

    def __init__(self, name, client_id, client_secret, client_auth_token="", user_auth_code="", user_auth_token="", user_refresh_token=""):
        self.name = name
        self.client_id = client_id
        self.client_secret = client_secret
        self.client_auth_token = client_auth_token
        self.user_auth_code = user_auth_code
        self.user_auth_token = user_auth_token
        self.user_refresh_token = user_refresh_token

        self.client_utils = Client(self.name, self.client_id, self.client_secret, self.client_auth_token)
        self.user_auth_utils = UserAuth(self.name, self.user_auth_token, self.user_refresh_token, self.client_id, self.client_secret)
        self.user_utils = User(self.user_auth_utils)
        self.track_utils = Track(self.client_utils)
        self.playlist_utils = Playlist(self.client_utils, self.user_auth_utils, self.user_utils)
        self.custom_utils = Custom(self.playlist_utils)

        if not os.path.isfile(f"app_info/{self.name}.json"):
            with open(f"app_info/{self.name}.json", 'w') as file:
                template = { 
                    "client_id": self.client_id, 
                    "client_secret": self.client_secret, 
                    "client_auth_token": self.client_auth_token, 
                    "user_auth_code": self.user_auth_code, 
                    "user_auth_token": self.user_auth_token,
                    "user_refresh_token": self.user_refresh_token
                }
                json_object = json.dumps(template, indent=4)
                file.write(json_object)
        else:
            with open(f"app_info/{self.name}.json", 'r') as file:
                read_dict = json.loads(file.read())
            write_dict = { "client_id": self.client_id, "client_secret": self.client_secret, "client_auth_token": self.client_auth_token, "user_auth_code": self.user_auth_code, "user_auth_token": self.user_auth_token}
            for key in write_dict:
                if key not in read_dict.keys():
                    read_dict[key] = write_dict[key]
                elif key in read_dict and read_dict[key] == "":
                    read_dict[key] = write_dict[key]
                write_json = json.dumps(read_dict, indent=4)
            with open(f"app_info/{self.name}.json", 'w') as file:
                file.write(write_json)