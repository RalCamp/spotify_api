import json
import os

from app_files.client_utils import Client
from app_files.user_auth_utils import UserAuth
from app_files.user_utils import User
from app_files.artist_utils import Artist
from app_files.track_utils import Track
from app_files.playlist_utils import Playlist
from app_files.custom_utils import Custom

class SpotifyApp():

    def __init__(self, app_name, client_id, client_secret, client_auth_token="", user_id="", user_auth_code="", user_auth_token="", user_refresh_token=""):
        self.app_name = app_name
        self.client_id = client_id
        self.client_secret = client_secret
        self.client_auth_token = client_auth_token
        self.user_id = user_id
        self.user_auth_code = user_auth_code
        self.user_auth_token = user_auth_token
        self.user_refresh_token = user_refresh_token

        print("Initialising app...")

        if not os.path.isdir("app_files/app_info"):
            print("Creating app_info directory...")
            os.mkdir("app_files/app_info")

        if not os.path.isfile(f"app_files/app_info/{self.app_name}.json"):
            print("Creating app data...")
            with open(f"app_files/app_info/{self.app_name}.json", 'w') as file:
                template = { 
                    "client_id": self.client_id, 
                    "client_secret": self.client_secret, 
                    "client_auth_token": self.client_auth_token, 
                    "user_id": self.user_id,
                    "user_auth_code": self.user_auth_code, 
                    "user_auth_token": self.user_auth_token,
                    "user_refresh_token": self.user_refresh_token
                }
                json_object = json.dumps(template, indent=4)
                file.write(json_object)
        else:
            print("Reading app data...")
            with open(f"app_files/app_info/{self.app_name}.json", 'r') as file:
                read_dict = json.loads(file.read())
            write_dict = { "client_id": self.client_id, "client_secret": self.client_secret, "client_auth_token": self.client_auth_token, "user_id": self.user_id, "user_auth_code": self.user_auth_code, "user_auth_token": self.user_auth_token}
            for key in write_dict:
                if key not in read_dict.keys():
                    read_dict[key] = write_dict[key]
                elif key in read_dict and read_dict[key] == "":
                    read_dict[key] = write_dict[key]
                write_json = json.dumps(read_dict, indent=4)
            with open(f"app_files/app_info/{self.app_name}.json", 'w') as file:
                file.write(write_json)

        if self.user_id == "":
            print("Reading user id...")
            with open(f"app_files/app_info/{self.app_name}.json", 'r') as file:
                read_dict = json.loads(file.read())
            if read_dict['user_id'] != "":
                self.user_id = read_dict['user_id']

        print("Initialising sub-classes...")
        
        self.client_utils = Client(self.app_name, self.client_id, self.client_secret, self.client_auth_token)
        self.user_auth_utils = UserAuth(self.app_name, self.user_auth_token, self.user_refresh_token, self.client_id, self.client_secret)
        self.user_utils = User(self.user_id, self.user_auth_utils)
        self.artist_utils = Artist(self.client_utils)
        self.track_utils = Track(self.client_utils, self.user_auth_utils)
        self.playlist_utils = Playlist(self.app_name, self.client_utils, self.user_auth_utils, self.user_utils, self.artist_utils, self.track_utils)
        self.custom_utils = Custom(self.playlist_utils)

        print("App initialised\n")