import requests
import time

from app_files.response_utils import Response

class User():
    def __init__(self, user_id, userauth):
        self.user_id = user_id
        self.userauth = userauth

    def get_user_info(self):
        self.userauth.manage_userauth_creds()
        hdrs = {
            "Authorization": f"Bearer {self.userauth.return_user_auth_token()}",
            "scope": "user-read-private"
        }
        r = requests.get('https://api.spotify.com/v1/me', headers=hdrs)
        if Response.request_successful(r):
            return r.json()
        else:
            Response.error_message(r)

    def get_user_top_artists(self, time_range=''):
        if time_range not in ['long_term', 'medium_term', 'short_term', '']:
            print("##############################################################################################")
            print("time_range must be one of: long_term (~1 year), medium_term (~6 months), short_term (~4 weeks)")
            print("##############################################################################################\n")
            return
        elif time_range == '':
            time_range = 'medium_term'
        self.userauth.manage_userauth_creds()
        hdrs = {
            "Authorization": f"Bearer {self.userauth.return_user_auth_token()}",
            "scope": "user-top-read"
        }
        r = requests.get(f"https://api.spotify.com/v1/me/top/artists?time_range={time_range}&limit=50", headers=hdrs)
        if not Response.request_successful(r):
            Response.error_message(r)  
            return None
        artists = r.json()
        top_artists = []
        while artists["next"] != None:
            for artist in artists['items']:
                top_artists.append(artist)
            time.sleep(1)
            r = requests.get(artists["next"], headers=hdrs)
            if not Response.request_successful(r):
                Response.error_message(r)  
                return None
            artists = r.json()
        for artist in artists['items']:
            top_artists.append(artist)
        return top_artists
    
    def user_top_artists_ranked(self, time_range, print_results=False):
        top_artists = self.get_user_top_artists(time_range)
        ranked = {}
        position = 1
        for artist in top_artists:
            ranked[position] = artist['name']
            position += 1
        if print_results:
            for key in ranked.keys():
                print(f"#{key}: {ranked[key]}")
        return ranked

    def get_user_top_tracks(self, time_range=''):
        if time_range not in ['long_term', 'medium_term', 'short_term', '']:
            print("##############################################################################################")
            print("time_range must be one of: long_term (~1 year), medium_term (~6 months), short_term (~4 weeks)")
            print("##############################################################################################\n")
            return
        elif time_range == '':
            time_range = 'medium_term'
        self.userauth.manage_userauth_creds()
        hdrs = {
            "Authorization": f"Bearer {self.userauth.return_user_auth_token()}",
            "scope": "user-top-read"
        }
        r = requests.get(f"https://api.spotify.com/v1/me/top/tracks?time_range={time_range}&limit=50", headers=hdrs)
        if not Response.request_successful(r):
            Response.error_message(r)  
            return None
        tracks = r.json()
        top_tracks = []
        while tracks["next"] != None:
            for track in tracks['items']:
                top_tracks.append(track)
            time.sleep(1)
            r = requests.get(tracks["next"], headers=hdrs)
            if not Response.request_successful(r):
                Response.error_message(r)  
                return None
            tracks = r.json()
        for track in tracks['items']:
            top_tracks.append(track)
        return top_tracks
    
    def user_top_tracks_ranked(self, time_range, print_results=False, range=0):
        top_tracks = self.get_user_top_tracks(time_range)
        ranked = {}
        position = 1
        for track in top_tracks:
            ranked[position] = track['name']
            position += 1
            if range > 0 and position > range:
                break
        if print_results:
            for key in ranked.keys():
                print(f"#{key}: {ranked[key]}")
        return ranked
    
    def get_user_playlists(self, user_owned_only=True, print_results=False):
        self.userauth.manage_userauth_creds()
        uri_list = []
        playlist_dict = {}
        hdrs = {
            "Authorization": f"Bearer {self.userauth.return_user_auth_token()}"
        }
        r = requests.get(f"https://api.spotify.com/v1/users/{self.user_id}/playlists?limit=50", headers=hdrs)
        if not Response.request_successful(r):
            Response.error_message(r)  
            return None
        playlists = r.json()
        while playlists["next"] != None:
            for playlist in playlists['items']:
                if user_owned_only:
                    if playlist['owner']['id'] == self.user_id:
                        uri_list.append(playlist['id'])
                        playlist_dict[playlist['name']] = playlist['id']
                else:
                    uri_list.append(playlist['id'])
                    playlist_dict[playlist['name']] = playlist['id']
            time.sleep(1)
            r = requests.get(playlists["next"], headers=hdrs)
            if not Response.request_successful(r):
                Response.error_message(r)  
                return None
            playlists = r.json()
        for playlist in playlists['items']:
            if user_owned_only:
                if playlist['owner']['id'] == self.user_id:
                    uri_list.append(playlist['id'])
                    playlist_dict[playlist['name']] = playlist['id']
            else:
                uri_list.append(playlist['id'])
                playlist_dict[playlist['name']] = playlist['id']
        if print_results:
            for playlist_name in playlist_dict.keys():
                print(f"{playlist_name} ({playlist_dict[playlist_name]})")
        return uri_list
