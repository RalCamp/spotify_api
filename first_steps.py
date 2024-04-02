# deps
import requests
import os
import json
import base64
import math
import time

class Spotify_App():

    def __init__(self, name, client_id, client_secret, client_auth_token="", user_auth_code="", user_auth_token="", user_refresh_token=""):
        self.name = name
        self.client_id = client_id
        self.client_secret = client_secret
        self.client_auth_token = client_auth_token
        self.user_auth_code = user_auth_code
        self.user_auth_token = user_auth_token
        self.user_refresh_token = user_refresh_token
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

    def read_client_auth_token(self):
        with open(f"app_info/{self.name}.json", 'r') as file:
            read_dict = json.loads(file.read())
        self.client_auth_token = read_dict["client_auth_token"]

    def read_user_auth_token(self):
        with open(f"app_info/{self.name}.json", 'r') as file:
            read_dict = json.loads(file.read())
        self.user_auth_token = read_dict["user_auth_token"]

    def read_user_refresh_token(self):
        with open(f"app_info/{self.name}.json", 'r') as file:
            read_dict = json.loads(file.read())
        self.user_refresh_token = read_dict["user_refresh_token"]

    def write_client_auth_token(self):
        with open(f"app_info/{self.name}.json", 'r') as file:
            read_dict = json.loads(file.read())
        read_dict["client_auth_token"] = self.client_auth_token
        write_json = json.dumps(read_dict, indent=4)
        with open(f"app_info/{self.name}.json", 'w') as file:
            file.write(write_json)

    def write_user_auth_token(self):
        with open(f"app_info/{self.name}.json", 'r') as file:
            read_dict = json.loads(file.read())    
        read_dict["user_auth_token"] = self.user_auth_token
        write_json = json.dumps(read_dict, indent=4)
        with open(f"app_info/{self.name}.json", 'w') as file:
            file.write(write_json)

    def write_user_refresh_token(self):
        with open(f"app_info/{self.name}.json", 'r') as file:
            read_dict = json.loads(file.read())    
        read_dict["user_refresh_token"] = self.user_refresh_token
        write_json = json.dumps(read_dict, indent=4)
        with open(f"app_info/{self.name}.json", 'w') as file:
            file.write(write_json)

    def request_successful(self, response_object):
        if response_object.status_code == 200 or response_object.status_code == 201:
            return True
        else:
            return False
        
    def error_message(self, response_object):
        print("##################################################")
        print("This request has resulted in a unexpected response\nThe response status code was: " + str(response_object.status_code))
        print(response_object.json()["error"]["message"])
        if response_object.status_code == 429:
            print(response_object.headers)
        print("##################################################")

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
    
    # this has been done via postman
    # def get_user_auth_token(self):
    #     encoded_credentials = base64.b64encode(self.client_id.encode() + b':' + self.client_secret.encode()).decode("utf-8")
    #     token_headers = {
    #         "Authorization": "Basic " + encoded_credentials,
    #         "Content-Type": "application/x-www-form-urlencoded"
    #     }
    #     token_params = {
    #         "grant_type": "authorization_code",
    #         "code": self.user_auth_code,
    #         "redirect_uri": "http://localhost:7777/callback"
    #     }
    #     r = requests.post("https://accounts.spotify.com/api/token", params=token_params, headers=token_headers)
    #     if self.request_successful(r):
    #         self.user_auth_token = r.json()["access_token"]
    #         self.write_user_auth_token()
    #         return r.json()
    #     else:
    #         self.error_message(r)

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
            elif self.request_successful(r):
                return False
            else:
                self.error_message(r)

    def user_auth_token_expired(self):
        self.read_user_auth_token()
        hdrs = {
            "Authorization": f"Bearer {self.user_auth_token}",
            "scope": "user-read-private"
        }
        r = requests.get('https://api.spotify.com/v1/me', headers=hdrs)
        if r.status_code == 401:
            return True
        elif self.request_successful(r):
            return False
        else:
            self.error_message(r)
        
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
        if self.request_successful(r):
            self.user_refresh_token = r.json()['refresh_token']
            self.write_user_refresh_token()
            return r.json()
        else:
            self.error_message()

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
        if self.request_successful(r):
            self.user_auth_token = r.json()["access_token"]
            self.write_user_auth_token()
            return r.json()
        else:
            self.error_message(r)
    
    def get_user_info(self):
        self.read_user_auth_token
        if self.user_auth_token_expired():
            self.user_auth_token_from_refresh_token()
        hdrs = {
            "Authorization": f"Bearer {self.user_auth_token}",
            "scope": "user-read-private"
        }
        r = requests.get('https://api.spotify.com/v1/me', headers=hdrs)
        if self.request_successful(r):
            return r.json()
        else:
            self.error_message(r)

    def get_playlist(self, playlist_id):
        if self.client_token_expired():
            self.get_client_auth_token()
        hdrs = {
            "Authorization": f"Bearer {self.client_auth_token}"
        }
        r = requests.get(f"https://api.spotify.com/v1/playlists/{playlist_id}", headers=hdrs)
        if self.request_successful(r):
            return r.json()
        else:
            self.error_message(r)

    def playlist_exist(self, playlist_id):
        if self.client_token_expired():
            self.get_client_auth_token()
        hdrs = {
            "Authorization": f"Bearer {self.client_auth_token}"
        }
        r = requests.get(f"https://api.spotify.com/v1/playlists/{playlist_id}", headers=hdrs)
        if self.request_successful(r):
            return True
        else:
            return False
    
    def get_playlist_tracks(self, playlist_id):
        if self.client_token_expired():
            self.get_client_auth_token()
        hdrs = {
            "Authorization": f"Bearer {self.client_auth_token}"
        }
        r = requests.get(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?limit=100", headers=hdrs)
        if not self.request_successful(r):
            self.error_message(r)  
            return None
        playlist = r.json()
        tracks = []
        while playlist["next"] != None:
            for item in playlist['items']:
                track = {}
                track['name'] = item['track']['name']
                track['uri'] = item['track']['uri']
                track['artists'] = [ artist['name'] for artist in item['track']['artists']]
                track['album'] = item['track']['album']['name']
                tracks.append(track)
            time.sleep(3)
            r = requests.get(playlist["next"], headers=hdrs)
            if not self.request_successful(r):
                self.error_message(r)  
                return None
            playlist = r.json()
        for item in playlist['items']:
            track = {}
            track['name'] = item['track']['name']
            track['uri'] = item['track']['uri']
            track['artists'] = [ artist['name'] for artist in item['track']['artists']]
            track['album'] = item['track']['album']['name']
            tracks.append(track)
        return tracks     
    
    def get_playlist_track_uris(self, playlist_id):
        playlist_tracks = self.get_playlist_tracks(playlist_id)
        uris = []
        for track in playlist_tracks:
            uris.append(track['uri'])
        return uris 
    
    def create_playlist(self, name, public=False, collaborative=False, description=""):
        self.read_user_auth_token
        if self.user_auth_token_expired():
            self.user_auth_token_from_refresh_token()
        user_id = self.get_user_info()["id"]
        user_endpoint = f"https://api.spotify.com/v1/users/{user_id}/playlists"
        hdrs = {
            "Authorization": f"Bearer {self.user_auth_token}"
        }
        payload = json.dumps({
            "name": name,
            "public": public,
            "collaborative": collaborative,
            "description": description
        })
        r = requests.post(user_endpoint, headers=hdrs, data=payload)
        if self.request_successful(r):
            if not os.path.isfile(f"app_info/created_playlists_{self.name}.json"):
                with open(f"app_info/created_playlists_{self.name}.json", "w") as file:
                    request_return = r.json()
                    item = {
                        request_return["id"]: {
                            "name": request_return["name"]
                        }
                    }
                    item_json = json.dumps(item, indent=4)
                    file.write(item_json)
            else: 
                with open(f"app_info/created_playlists_{self.name}.json", "r") as file:
                    playlists_dict = json.loads(file.read())
                request_return = r.json()
                if request_return["id"] not in playlists_dict.keys():
                    playlists_dict[request_return["id"]] = {"name": request_return["name"]}
                    playlists_json = json.dumps(playlists_dict, indent=4)
                    with open(f"app_info/created_playlists_{self.name}.json", "w") as file:
                        file.write(playlists_json)
            return r.json()
        else:
            self.error_message(r)

    def created_playlist_cleanup(self):
        with open(f"app_info/created_playlists_{self.name}.json", "r") as file:
            playlists_dict = json.loads(file.read())
        for id in playlists_dict.keys():
            if not self.playlist_exist(id):
                playlists_dict.pop(id)
        playlists_json = json.dumps(playlists_dict, indent=4)
        with open(f"app_info/created_playlists_{self.name}.json", "w") as file:
            file.write(playlists_json)
        return playlists_json
    
    def append_tracks_to_playlist(self, playlist_id, uris, duplicates=False):
        self.read_user_auth_token
        if self.user_auth_token_expired():
            self.user_auth_token_from_refresh_token()
        hdrs = {
            "Authorization": f"Bearer {self.user_auth_token}",
            "Content-Type": "application/json"
        }
        tracks_to_append = []
        for uri in uris:
            if duplicates:
                if uri.find("spotify:track:") == -1:
                    tracks_to_append.append(f"spotify:track:{uri}")
                else:
                    tracks_to_append.append(uri)
            else:
                if uri.find("spotify:track:") == -1:
                    uri_formatted = f"spotify:track:{uri}"
                else:
                    uri_formatted = uri

                if uri_formatted not in self.get_playlist_track_uris(playlist_id):
                    tracks_to_append.append(uri_formatted)
        # you can only add 100 items per request https://developer.spotify.com/documentation/web-api/reference/add-tracks-to-playlist
        if len(tracks_to_append) == 0:
            print("#########################################################")
            print("After removing duplicates there are no tracks left to add")
            print("#########################################################")
        elif len(tracks_to_append) <= 100:
            payload = {
                "uris": tracks_to_append
            }
            payload_json = json.dumps(payload)
            r = requests.post(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks", headers=hdrs, data=payload_json)
            if self.request_successful(r):
                return r.json()
            else:
                self.error_message(r)
        else:
            slices = math.ceil(len(tracks_to_append) / 100)
            for n in range(1, (slices)):
                print(f"Adding tracks (operation {n} of {slices})...")
                time.sleep(3)
                lower_slice = 0 + (100 * (n - 1))
                upper_slice = 100 + (100 * (n - 1))
                payload = {
                    "scope": "playlist-modify-private",
                    "uris": tracks_to_append[lower_slice:upper_slice]
                }
                payload_json = json.dumps(payload)
                r = requests.post(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks", headers=hdrs, data=payload_json)
                if not self.request_successful(r):
                    self.error_message(r)
            print(f"Adding tracks (operation {slices} of {slices})...")
            final_lower = 100 * (slices - 1)
            if final_lower != []:
                payload = {
                    "uris": tracks_to_append[final_lower::]
                }
                r = requests.post(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks", headers=hdrs, data=payload)
                if not self.request_successful(r):
                    self.error_message(r)
            print("Tracks added")

    def append_playlists_to_playlist(self, playlist, playlists_to_append, duplicates=False, log_added_tracks=False):
        tracks_to_append = []
        print("Collecting tracks to add...")
        if duplicates == False:
            playlist_tracks = self.get_playlist_track_uris(playlist)
            for playlist_to_append in playlists_to_append:
                print("Getting playlist information...")
                time.sleep(3)
                uris = self.get_playlist_track_uris(playlist_to_append)
                for uri in uris:
                    if uri not in playlist_tracks and uri not in tracks_to_append:
                        tracks_to_append.append(uri)
        else:
            for playlist_to_append in playlists_to_append:
                print("Getting playlist information...")
                time.sleep(3)
                uris = self.get_playlist_track_uris(playlist_to_append)
                for uri in uris:
                    tracks_to_append.append(uri)
        if log_added_tracks == True:
            if not os.path.isfile(f"app_info/{playlist}_added_tracks.json"):
                with open(f"app_info/{playlist}_added_tracks.json", 'w') as file:
                    added_tracks = json.dumps(tracks_to_append, indent=4)
                    file.write(added_tracks)
            else:
                with open(f"app_info/{playlist}_added_tracks.json", 'r') as file:
                    added_tracks = json.loads(file.read())
                for track in added_tracks:
                    if track in tracks_to_append:
                        tracks_to_append.remove(track)
                if tracks_to_append != []:
                    for track in tracks_to_append:
                        added_tracks.append(track)
                print("Logging added tracks...")
                added_tracks_json = json.dumps(added_tracks, indent=4)
                with open(f"app_info/{playlist}_added_tracks.json", 'w') as file:
                    file.write(added_tracks_json)
        if tracks_to_append == []:
            print("#########################################################")
            print("After removing duplicates there are no tracks left to add")
            print("#########################################################")
            return None
        print(f"Adding {str(len(tracks_to_append))} tracks...")
        # we've already dealt with potential duplicates here, so we don't need to do it again
        self.append_tracks_to_playlist(playlist, tracks_to_append, duplicates=True)

                



first_app = Spotify_App("66768cc0e0fb4cc5a9ae5421aa6c399c", "644255b4d32e4644a3b25009a35b0dfb")
print(first_app.__dict__)
print(first_app.get_auth_token())
print(first_app.get_playlist_tracks("0eZ4xWjBofNncbo5p5n2zn?si=6350fa5fc41143fe"))
print(first_app.__dict__)
print(first_app.append_tracks_to_playlist("0eZ4xWjBofNncbo5p5n2zn?si=6350fa5fc41143fe", ["0bM9c5A7CterSOEssmWqAa", "5LyRtsQLhcXmy50VXhQXXS"]))