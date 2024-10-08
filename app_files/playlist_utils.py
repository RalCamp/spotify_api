import requests
import json
import os
import time
import math
import numpy as np # type: ignore
from scipy import stats # type: ignore
from datetime import datetime
from app_files.response_utils import Response

class Playlist():
    def __init__(self, app_name, client, userauth, user, artist, track):
        self.app_name = app_name
        self.client = client
        self.userauth = userauth
        self.user = user
        self.artist = artist
        self.track = track

    def playlist_exist(self, playlist_id):
        self.client.manage_client_creds()
        hdrs = {
            "Authorization": f"Bearer {self.client.return_client_auth_token()}"
        }
        r = requests.get(f"https://api.spotify.com/v1/playlists/{playlist_id}", headers=hdrs)
        if Response.request_successful(r):
            return True
        else:
            return False

    def get_playlist(self, playlist_id):
        self.client.manage_client_creds()
        hdrs = {
            "Authorization": f"Bearer {self.client.return_client_auth_token()}"
        }
        r = requests.get(f"https://api.spotify.com/v1/playlists/{playlist_id}", headers=hdrs)
        if Response.request_successful(r):
            return r.json()
        else:
            Response.error_message(r)
    
    def get_playlist_tracks(self, playlist_id):
        self.client.manage_client_creds()
        hdrs = {
            "Authorization": f"Bearer {self.client.return_client_auth_token()}"
        }
        r = requests.get(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?limit=100", headers=hdrs)
        if not Response.request_successful(r):
            Response.error_message(r)  
            return None
        playlist = r.json()
        tracks = []
        while playlist["next"] != None:
            for item in playlist['items']:
                track = {}
                track['name'] = item['track']['name']
                track['id'] = item['track']['id']
                track['artists'] = [ artist['name'] for artist in item['track']['artists']]
                track['album'] = item['track']['album']['name']
                track['popularity'] = item['track']['popularity']
                tracks.append(track)
            time.sleep(1)
            r = requests.get(playlist["next"], headers=hdrs)
            if not Response.request_successful(r):
                Response.error_message(r)  
                return None
            playlist = r.json()
        for item in playlist['items']:
            track = {}
            track['name'] = item['track']['name']
            track['id'] = item['track']['id']
            track['artists'] = [ artist['name'] for artist in item['track']['artists']]
            track['album'] = item['track']['album']['name']
            track['popularity'] = item['track']['popularity']
            tracks.append(track)
        return tracks     
    
    def get_playlist_track_uris(self, playlist_id):
        playlist_tracks = self.get_playlist_tracks(playlist_id)
        uris = []
        for track in playlist_tracks:
            uris.append(track['id'])
        return uris
    
    def get_playlist_artists(self, playlist_id, unique_artists=True):
        self.client.manage_client_creds()
        hdrs = {
            "Authorization": f"Bearer {self.client.return_client_auth_token()}"
        }
        r = requests.get(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?limit=100", headers=hdrs)
        if not Response.request_successful(r):
            Response.error_message(r)  
            return None
        playlist = r.json()
        artists = []
        while playlist["next"] != None:
            for item in playlist['items']:
                for artist in item['track']['artists']:
                    if unique_artists == True and artist['id'] not in artists:
                        artists.append(artist['id'])
                    else:
                        artists.append(artist['id'])
            time.sleep(1)
            r = requests.get(playlist["next"], headers=hdrs)
            if not Response.request_successful(r):
                Response.error_message(r)  
                return None
            playlist = r.json()
        for item in playlist['items']:
            for artist in item['track']['artists']:
                if unique_artists == True and artist['id'] not in artists:
                    artists.append(artist['id'])
                else:
                    artists.append(artist['id'])
        return artists
    
    def create_playlist(self, name, public=False, collaborative=False, description=""):
        self.userauth.manage_userauth_creds()
        user_id = self.user.get_user_info()["id"]
        user_endpoint = f"https://api.spotify.com/v1/users/{user_id}/playlists"
        hdrs = {
            "Authorization": f"Bearer {self.userauth.return_user_auth_token()}"
        }
        payload = json.dumps({
            "name": name,
            "public": public,
            "collaborative": collaborative,
            "description": description
        })
        r = requests.post(user_endpoint, headers=hdrs, data=payload)
        if Response.request_successful(r):
            if not os.path.isfile(f"app_files/app_info/created_playlists_{self.app_name}.json"):
                with open(f"app_files/app_info/created_playlists_{self.app_name}.json", "w") as file:
                    request_return = r.json()
                    item = {
                        request_return["id"]: {
                            "name": request_return["name"]
                        }
                    }
                    item_json = json.dumps(item, indent=4)
                    file.write(item_json)
            else: 
                with open(f"app_files/app_info/created_playlists_{self.app_name}.json", "r") as file:
                    playlists_dict = json.loads(file.read())
                request_return = r.json()
                if request_return["id"] not in playlists_dict.keys():
                    playlists_dict[request_return["id"]] = {"name": request_return["name"]}
                    playlists_json = json.dumps(playlists_dict, indent=4)
                    with open(f"app_files/app_info/created_playlists_{self.app_name}.json", "w") as file:
                        file.write(playlists_json)
            return r.json()
        else:
            Response.error_message(r)

    def created_playlist_cleanup(self):
        with open(f"app_files/app_info/created_playlists_{self.app_name}.json", "r") as file:
            playlists_dict = json.loads(file.read())
        print(f"Checking the contents of created_playlists_{self.app_name}.json...")
        for id in playlists_dict.keys():
            if not self.playlist_exist(id):
                print(f"{playlists_dict['id']['name']} no longer exists\nRemoving playlist from created_playlists_{self.app_name}.json...")
                playlists_dict.pop(id)
        playlists_json = json.dumps(playlists_dict, indent=4)
        with open(f"app_files/app_info/created_playlists_{self.app_name}.json", "w") as file:
            file.write(playlists_json)
        print(f"The contents of created_playlists_{self.app_name}.json has been updated\n")
        return playlists_json

    def edit_playlist_details(self, playlist_id, new_title=None, public=None, collaborative=None, description=None):
        self.userauth.manage_userauth_creds()
        playlist_name = self.get_playlist(playlist_id)['name']
        print(f"Updating details for {playlist_name}...")
        hdrs = {
            "Authorization": f"Bearer {self.userauth.return_user_auth_token()}",
            "Content-Type": "application/json"
        }
        payload_dict = {}
        if new_title != None:
            payload_dict['name'] = new_title
        if public != None:
            payload_dict['public'] = public
        if collaborative != None:
            payload_dict['collaborative'] = collaborative
        if description != None:
            payload_dict['description'] = description
        payload = json.dumps(payload_dict)
        r = requests.put(f"https://api.spotify.com/v1/playlists/{playlist_id}", headers=hdrs, data=payload)
        if Response.request_successful(r):
            print("The details of this playlist have been updated\n")
        else:
            Response.error_message(r)
    
    def append_tracks_to_playlist(self, playlist_id, uris, duplicates=False):
        self.userauth.manage_userauth_creds()
        hdrs = {
            "Authorization": f"Bearer {self.userauth.return_user_auth_token()}",
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
            print("#########################################################\n")
        elif len(tracks_to_append) <= 100:
            payload = {
                "uris": tracks_to_append
            }
            payload_json = json.dumps(payload)
            print("Adding tracks...")
            r = requests.post(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks", headers=hdrs, data=payload_json)
            if Response.request_successful(r):
                print("Tracks added\n")
                return r.json()
            else:
                Response.error_message(r)
        else:
            slices = math.ceil(len(tracks_to_append) / 100)
            for n in range(1, (slices)):
                print(f"Adding tracks (operation {n} of {slices})...")
                time.sleep(1)
                lower_slice = 0 + (100 * (n - 1))
                upper_slice = 100 + (100 * (n - 1))
                payload = {
                    "uris": tracks_to_append[lower_slice:upper_slice]
                }
                payload_json = json.dumps(payload)
                r = requests.post(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks", headers=hdrs, data=payload_json)
                if not Response.request_successful(r):
                    Response.error_message(r)
            print(f"Adding tracks (operation {slices} of {slices})...")
            final_lower = 100 * (slices - 1)
            if final_lower != []:
                payload = {
                    "uris": tracks_to_append[final_lower::]
                }
                payload_json = json.dumps(payload)
                r = requests.post(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks", headers=hdrs, data=payload_json)
                if not Response.request_successful(r):
                    Response.error_message(r)
                else:
                    print("Tracks added\n")

    def remove_tracks_from_playlist(self, playlist_id, tracks_to_remove):
        self.userauth.manage_userauth_creds()
        hdrs = {
            "Authorization": f"Bearer {self.userauth.return_user_auth_token()}",
            "Content-Type": "application/json"
        }
        playlist_name = self.get_playlist(playlist_id)['name']
        print(f"Removing tracks from {playlist_name}...")
        print(f"Getting current tracks from {playlist_name}...")
        tracks_in_playlist = self.get_playlist_track_uris(playlist_id)
        print("Checking format of supplied tracks...")
        tracks_to_remove_formatted = []
        for track in tracks_to_remove:
            if track in tracks_in_playlist:
                if track.find("spotify:track:") == -1:
                    track = "spotify:track:" + track
                item_to_add = {}
                item_to_add['uri'] = track
                tracks_to_remove_formatted.append(item_to_add)
        tracks_to_remove = tracks_to_remove_formatted
        if len(tracks_to_remove) == 0:
            print("#####################################################################################")
            print(f"None of these tracks are in {playlist_name}")
            print("#####################################################################################\n")
        elif len(tracks_to_remove) <= 100:
            payload = {
                "tracks": tracks_to_remove
            }
            payload_json = json.dumps(payload)
            print("Removing tracks...")
            r = requests.delete(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks", headers=hdrs, data=payload_json)
            if Response.request_successful(r):
                print("Tracks removed\n")
                return r.json()
            else:
                Response.error_message(r)
        else:
            slices = math.ceil(len(tracks_to_remove) / 100)
            for n in range(1, (slices)):
                print(f"Removing tracks (operation {n} of {slices})...")
                time.sleep(1)
                lower_slice = 0 + (100 * (n - 1))
                upper_slice = 100 + (100 * (n - 1))
                payload = {
                    "tracks": tracks_to_remove[lower_slice:upper_slice]
                }
                payload_json = json.dumps(payload)
                r = requests.delete(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks", headers=hdrs, data=payload_json)
                if not Response.request_successful(r):
                    Response.error_message(r)
            print(f"Removing tracks (operation {slices} of {slices})...")
            final_lower = 100 * (slices - 1)
            if final_lower != []:
                payload = {
                    "uris": tracks_to_remove[final_lower::]
                }
                payload_json = json.dumps(payload)
                r = requests.delete(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks", headers=hdrs, data=payload_json)
                if not Response.request_successful(r):
                    Response.error_message(r)
            print(f"Tracks removed from {playlist_name}\n")
            
    def find_potential_duplicates(self, playlist_id, check_artists=False):
        self.client.manage_client_creds()
        self.userauth.manage_userauth_creds()
        if check_artists:
            print("Note that this checks track names and artists only - manual verification is required")
        else:
            print("Note that this checks track names only - manual verification is required")
        playlist_tracks = self.get_playlist_tracks(playlist_id)
        potential_duplicates = {}
        print("Checking tracks...")
        for track in playlist_tracks:
            name_to_check = track['name']
            atrists_to_check = track['artists']
            count = 0
            if check_artists:
                for track in playlist_tracks:
                    if track['name'] == name_to_check and track['artists'] == atrists_to_check:
                        count += 1
            else:
                for track in playlist_tracks:
                    if track['name'] == name_to_check:
                        count += 1
            if count > 1 and name_to_check not in potential_duplicates:
                potential_duplicates[name_to_check] = count
        if potential_duplicates == {}:
            print("#############################################")
            print("Unable to find any potential duplicate tracks")
            print("#############################################\n")
        elif len(potential_duplicates) == 1:
            print(f"There is 1 potential duplicate track in this playlist - it is:")
            for track in potential_duplicates.keys():
                print(track)
            print()
        else:
            print(f"There are {len(potential_duplicates)} potential duplicate tracks in this playlist - they are:")
            for track in potential_duplicates.keys():
                print(track)
            print()

    def append_playlists_to_playlist(self, playlist, playlists_to_append, duplicates=False, log_added_tracks=False):
        tracks_to_append = []
        playlist_name = self.get_playlist(playlist)['name']
        print(f"Collecting tracks to add to {playlist_name}...")
        if duplicates == False:
            print(f"Getting current tracks from {playlist_name}...")
            playlist_tracks = self.get_playlist_track_uris(playlist)
            for playlist_to_append in playlists_to_append:
                playlist_name = self.get_playlist(playlist_to_append)['name']
                print(f"Getting tracks from {playlist_name}...")
                time.sleep(1)
                uris = self.get_playlist_track_uris(playlist_to_append)
                for uri in uris:
                    if uri not in playlist_tracks and uri not in tracks_to_append:
                        tracks_to_append.append(uri)
        else:
            for playlist_to_append in playlists_to_append:
                playlist_name = self.get_playlist(playlist_to_append)['name']
                print(f"Getting tracks from {playlist_name}...")
                time.sleep(1)
                uris = self.get_playlist_track_uris(playlist_to_append)
                for uri in uris:
                    tracks_to_append.append(uri)
        if log_added_tracks == True:
            if not os.path.isfile(f"app_files/app_info/{playlist}_added_tracks.json"):
                with open(f"app_files/app_info/{playlist}_added_tracks.json", 'w') as file:
                    added_tracks = json.dumps(tracks_to_append, indent=4)
                    file.write(added_tracks)
            else:
                with open(f"app_files/app_info/{playlist}_added_tracks.json", 'r') as file:
                    added_tracks = json.loads(file.read())
                for track in added_tracks:
                    if track in tracks_to_append:
                        tracks_to_append.remove(track)
                if tracks_to_append != []:
                    for track in tracks_to_append:
                        added_tracks.append(track)
                    print("Logging added tracks...")
                    added_tracks_json = json.dumps(added_tracks, indent=4)
                    with open(f"app_files/app_info/{playlist}_added_tracks.json", 'w') as file:
                        file.write(added_tracks_json)
        if tracks_to_append == []:
            print("#########################################################")
            print("After removing duplicates there are no tracks left to add")
            print("#########################################################\n")
            return None
        print(f"Adding {str(len(tracks_to_append))} tracks...\n")
        # we've already dealt with potential duplicates here, so we don't need to do it again
        self.append_tracks_to_playlist(playlist, tracks_to_append, duplicates=True)

    def combine_playlists(self, playlists, current_playlist, create_new_playlist=False):
        if create_new_playlist:
            # I'd like this to create a new playlist if one doesn't already exist
            return None
        else:
            current_playlist_tracks = self.get_playlist_tracks(current_playlist)
            if current_playlist_tracks == []:
                current_playlist_tracks = []
            else:
                current_playlist_tracks = self.get_playlist_track_uris(current_playlist)
        combined_tracks = []
        tracks_to_remove = []
        for playlist in playlists:
            playlist_name = self.get_playlist(playlist)['name']
            print(f"Getting current tracks from {playlist_name}...")
            playlist_tracks = self.get_playlist_track_uris(playlist)
            for track in playlist_tracks:
                if track not in combined_tracks:
                    combined_tracks.append(track)
        print("Checking combined tracks against current playlist...")
        print("Determining which tracks are no longer in this playlist...")
        for track in current_playlist_tracks:
            if track not in combined_tracks:
                tracks_to_remove.append(track)
        print("Determining new tracks...")
        for track in current_playlist_tracks:
            if track in combined_tracks:
                combined_tracks.remove(track)
        if len(combined_tracks) == 0 and len(tracks_to_remove) == 0:
            print("###########################################")
            print("No changes need to be made to this playlist")
            print("###########################################\n")
        else:
            if len(combined_tracks) == 0:
                print("##############################")
                print("There are no new tracks to add")
                print("##############################")
            else:
                print("Adding new tracks...")
                self.append_tracks_to_playlist(current_playlist, combined_tracks, duplicates=True)
            if len(tracks_to_remove) == 0:
                print("#################################")
                print("There are no old tracks to remove")
                print("#################################")
            else:
                print("Removing old tracks...")
                self.remove_tracks_from_playlist(current_playlist, tracks_to_remove)
            print("The playlists have now been combined\n")

    def get_playlist_track_audio_features(self, playlist_id):
        self.client.manage_client_creds()
        playlist_name = self.get_playlist(playlist_id)['name']
        playlist_uris = self.get_playlist_track_uris(playlist_id)
        playlist_track_audio_features = {}
        print(f"Getting audio features for {len(playlist_uris)} tracks from {playlist_name}...")
        for uri in playlist_uris:
            time.sleep(1)
            playlist_track_audio_features[uri] = self.track.get_audio_features(uri)
        return playlist_track_audio_features
    
    def get_playlist_audio_features(self, playlist_id):
        playlist_track_audio_features = self.get_playlist_track_audio_features(playlist_id)
        playlist_audio_features = {
            "danceability": [],
            "energy": [],
            "loudness": [],
            "speechiness": [],
            "acousticness": [],
            "instrumentalness": [],
            "liveness": [],
            "valence": [],
            "tempo": []
        }
        for track in playlist_track_audio_features.keys():
            for feature in playlist_audio_features.keys():
                playlist_audio_features[feature].append(playlist_track_audio_features[track][feature])
        return playlist_audio_features
    
    def get_average_playlist_audio_features(self, playlist_id):
        playlist_audio_features = self.get_playlist_audio_features(playlist_id)
        playlist_averages = {}
        for feature in playlist_audio_features.keys():
            arr = np.array(playlist_audio_features[feature])
            data = {}
            data["mean"] = round(np.mean(arr), 3)
            data["median"] = np.median(arr)
            data["standard deviation"] = round(np.std(arr), 3)
            playlist_averages[feature] = data
        return playlist_averages

    def playlist_of_recommended_tracks(self, playlist_name="", limit=20, market=None, seeds={ 'seed_artists': [], 'seed_genres': [], 'seed_tracks': [] }, audio_features=None):
        self.client.manage_client_creds()
        self.userauth.manage_userauth_creds()
        if playlist_name == "":
            current_date = datetime.now().strftime("%d/%m/%y")
            playlist_name = f"Recommendations {current_date}"
        print("Getting recommendations...")
        recs = self.track.get_recommendations(limit, market, seeds, audio_features)
        if recs == None:
            return
        to_add = []
        for track in recs["tracks"]:
            to_add.append(track['id'])
        print("Creating playlist...")
        new_playlist = self.create_playlist(name=playlist_name)
        self.append_tracks_to_playlist(new_playlist["id"], to_add)
        return new_playlist["id"]
    
    def recommend_tracks_from_playlist(self, playlist_id, seed, use_audio_features=False, use_min_max=False, create_playlist=False):
        playlist_tracks = self.get_playlist_tracks(playlist_id)
        seeds={ 'seed_artists': [], 'seed_genres': [], 'seed_tracks': [] }
        if seed == 'artists':
            print("Using 5 most common playlist artists as seed...")
            artists = self.get_playlist_artists(playlist_id, unique_artists=False)
            artist_count = {}
            for artist in artists:
                if artist not in artist_count.keys():
                    artist_count[artist] = artists.count(artist)
            artists_sorted = [*dict(sorted(artist_count.items(), key=lambda item: item[1]))][::-1]
            seeds['seed_artists'] = artists_sorted[0:5]
        elif seed == 'genres':
            print("Using 5 most common playlist genres as seed...")
            genres = []
            genre_count = {}
            print("Getting playlist artists...")
            artists = self.get_playlist_artists(playlist_id, unique_artists=False)
            artist_count = 1
            for artist in artists:
                print (f"Getting genres for artist {artist_count} of {len(artists)}")
                artist_genres = self.artist.get_artist(artist)['genres']
                for genre in artist_genres:
                    genres.append(genre)
                artist_count += 1
            time.sleep(1)
            for genre in genres:
                if genre not in genre_count.keys():
                    genre_count[genre] = genres.count(genre)
            genres_sorted = [*dict(sorted(genre_count.items(), key=lambda item: item[1]))][::-1]
            seeds['seed_genres'] = genres_sorted[0:5]
        elif seed == 'tracks':
            print("Using 5 most popular playlist songs as seed...")
            tracks = {}
            for track in playlist_tracks:
                if track['id'] not in tracks.keys():
                    tracks[track['id']] = track['popularity']
            tracks_sorted = [*dict(sorted(tracks.items(), key=lambda item: item[1]))][::-1]
            if len(tracks_sorted) <= 5:
                seeds['seed_tracks'] = tracks_sorted
            else:
                seeds['seed_tracks'] = tracks_sorted[0:5]
        else:
            print("################################")
            print("ERROR - incorrect value for seed")
            print("seed must be one of:\n- artists\n- genres\n- tracks")
            print("################################")
            return
        if use_audio_features:
            average_audio_features = self.get_average_playlist_audio_features(playlist_id)
            audio_features = {}
            for feature in average_audio_features.keys():
                audio_features[f"target_{feature}"] = average_audio_features[feature]['mean']
                if use_min_max:
                    audio_features[f"min_{feature}"] = round(average_audio_features[feature]['mean'] - average_audio_features[feature]['standard deviation'], 3)
                    audio_features[f"max_{feature}"] = round(average_audio_features[feature]['mean'] + average_audio_features[feature]['standard deviation'], 3)
        else:
            audio_features = None
        if create_playlist:
            playlist_name = self.get_playlist(playlist_id)['name']
            self.playlist_of_recommended_tracks(playlist_name=f"{playlist_name} Recommendations", limit=100, seeds=seeds, audio_features=audio_features)
        else:
            recs = self.track.get_recommendations(100, None, seeds, audio_features)
            if recs == None:
                return
            else:
                return recs
        
    def filter_playlist_by_audio_features(self, playlist_id, audio_features, make_playlist=False):
        tracks = self.get_playlist_track_audio_features(playlist_id)
        playlist_name = self.get_playlist(playlist_id)['name']
        filtered_tracks = []
        print("Filtering tracks...")
        for key in tracks.keys():
            track = tracks[key]
            track_passes = True
            for feature in audio_features.keys():
                if "min" not in audio_features[feature].keys():
                    if track[feature] > audio_features[feature]["max"]:
                        track_passes = False
                elif "max" not in audio_features[feature].keys():
                    if track[feature] < audio_features[feature]["min"]:
                        track_passes = False
                else:
                    if track[feature] < audio_features[feature]["min"] or track[feature] > audio_features[feature]["max"]:
                        track_passes = False
            if track_passes:
                filtered_tracks.append(track['id'])
        if filtered_tracks == []:
            print("There do not appear to be any tracks in this playlist that are within the provided parameters\n")
            return None
        else:
            if make_playlist:
                print("")
                new_playlist_id = self.create_playlist(f"{playlist_name} Filtered", description=str(audio_features))["id"]
                self.append_tracks_to_playlist(new_playlist_id, filtered_tracks)
            else:
                return filtered_tracks
            