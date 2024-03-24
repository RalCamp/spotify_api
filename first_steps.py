# get an auth token, use that token to get a json of artist information for Justin Timberlake

# deps
import requests

class Spotify_App():

    def __init__(self, client_id, client_secret, access_token=""):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token

    def get_auth_token(self):
        payload = {
            "Content-Type": "application/x-www-form-urlencoded", 
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret
            }
        r = requests.post('https://accounts.spotify.com/api/token', data=payload)
        self.access_token = r.json()['access_token']

    def token_expired(self):
        expired = False
        if self.access_token == "":
            self.get_auth_token()
            return expired
        else:
            hdrs = {
                "Authorization": f"Bearer {self.access_token}"
            }
            r = requests.get('https://api.spotify.com/v1/me', headers=hdrs)
            response = r.status_code
            if response == 401:
                expired = True
                return expired
            elif response == 200:
                return expired
            else:
                print("##################################################")
                print("This request has resulted in a unexpected response\nThe response status code was: " + str(response))
                print("##################################################")

    def get_playlist(self, playlist_id):
        if self.token_expired():
            self.get_auth_token()
        hdrs = {
            "Authorization": f"Bearer {self.access_token}"
        }
        r = requests.get(f"https://api.spotify.com/v1/playlists/{playlist_id}", headers=hdrs)
        if r.status_code != 200:
            print("##################################################")
            print("This request has resulted in a unexpected response\nThe response status code was: " + str(r.status_code))
            print("##################################################")
        else:
            return r.json()
    
    def get_playlist_tracks(self, playlist_id):
        playlist = self.get_playlist(playlist_id)
        tracks = []
        for item in playlist['tracks']['items']:
            track = {}
            track['name'] = item['track']['name']
            track['uri'] = item['track']['uri']
            track['artists'] = [ artist['name'] for artist in item['track']['artists']]
            track['album'] = item['track']['album']['name']
            tracks.append(track)
        return tracks
    
    def get_uris(self, playlist_id):
        playlist = self.get_playlist(playlist_id)
        uris = []
        for item in playlist['tracks']['items']:
            uris.append(item['track']['uri'])
        return uris
    
    def append_tracks_to_playlist(self, playlist_id, uris, duplicates=False):
        if self.token_expired():
            self.get_auth_token()
        payload = {
            "Authorization": f"Bearer {self.access_token}",
            "scope": "playlist-modify-private",
            "uris": []
        }
        for uri in uris:
            if duplicates:
                if uri.find("spotify:track:") == -1:
                    payload["uris"].append(f"spotify:track:{uri}")
                else:
                    payload["uris"].append(uri)
            else:
                if uri.find("spotify:track:") == -1:
                    uri_formatted = f"spotify:track:{uri}"
                else:
                    uri_formatted = uri
    # # this is being held up by not being able to create playlists
    # def append_tracks_to_playlist(self, playlist_id, uris, duplicates=False):
    #     if self.token_expired():
    #         self.get_auth_token()
    #     payload = {
    #         "Authorization": f"Bearer {self.access_token}",
    #         "scope": "playlist-modify-private",
    #         "uris": []
    #     }
    #     for uri in uris:
    #         if duplicates:
    #             if uri.find("spotify:track:") == -1:
    #                 payload["uris"].append(f"spotify:track:{uri}")
    #             else:
    #                 payload["uris"].append(uri)
    #         else:
    #             if uri.find("spotify:track:") == -1:
    #                 uri_formatted = f"spotify:track:{uri}"
    #             else:
    #                 uri_formatted = uri

    #             if uri_formatted not in self.get_uris(playlist_id):
    #                 payload["uris"].append(uri_formatted)
    #     print(payload)
    #     r = requests.post(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks", data=payload)
    #     if r.status_code != 201:
    #         print("##################################################")
    #         print("This request has resulted in a unexpected response\nThe response status code was: " + str(r.status_code))
    #         print("##################################################")
    #     else:
    #         return self.get_playlist_tracks(playlist_id)


first_app = Spotify_App("66768cc0e0fb4cc5a9ae5421aa6c399c", "644255b4d32e4644a3b25009a35b0dfb")
print(first_app.__dict__)
print(first_app.get_auth_token())
print(first_app.get_playlist_tracks("0eZ4xWjBofNncbo5p5n2zn?si=6350fa5fc41143fe"))
print(first_app.__dict__)
print(first_app.append_tracks_to_playlist("0eZ4xWjBofNncbo5p5n2zn?si=6350fa5fc41143fe", ["0bM9c5A7CterSOEssmWqAa", "5LyRtsQLhcXmy50VXhQXXS"]))