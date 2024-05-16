# spotify_api

Please note that this is **only intended for personal use** with a personal instance of a Spotify app (see [Creating an App](#creating-an-app)). The current method of storing client/user secrets and auth tokens is **not secure**.

## Setup

### Creating an App

Instructions on how to do this can be found in the [Spotify web-api documentation](https://developer.spotify.com/documentation/web-api/tutorials/getting-started#create-an-app), but basically consist of the following steps:

1. Go to your dashboard via the profile link in the top right-hand corner of the screen

2. Click the *Create an app* button

3. Chose a name an description for your app

4. Set a Redirect URI - if your a planning on using Postman for initial user authentication (see [here](#user-authentication-via-postman)) then this should be set to `https://oauth.pstmn.io/v1/browser-callback`

5. Accept the *Developer Terms of Service*

6. Click *Create*

Your app should now be visible in your dashboard. Click on the app and go to *settings* to see your *Client ID* and *Client Secret* - these are required to successfully request an access token (referred to in this documentation as a [client auth token](#client_utils))

### User Authentication via Postman

This is slightly more complicated - details can be found [here](https://youtu.be/N34BM2CU_3g?si=9YqSgI5UlDCSKFWu). Note that the scope set required for this app to function correctly is currently `user-library-read playlist-read-private playlist-modify-private playlist-modify-public`. Following the steps in the link above will return an authentication token and a refresh token.

### App Initialisation

The `Spotify_App` class takes the following arguments:

- `app_name` (required): An arbitrary identifying string, used when storing information about the app.

- `client_id` (required): Found by going to your personal dashboard from the [Spotify web-api documentation](https://developer.spotify.com/documentation/web-api/concepts/api-calls), clicking on your app and going to *settings*.

- `client_secret` (required): See above. Used to authorise API calls.

- `client_auth_token` (optional, default value = ""): The authorisation token for your app, acquired and managed via [client_utils](#client_utils) functions.

- `user_id` (optional, default value = ""): The id associated with your user - required for [create_playlist()](#create_playlist) and [get_user_playlists()](#get_user_playlists). This id is not currently recovered automatically, but can be found using [get_user_info()](#get_user_info).

- `user_auth_code` (optional, default value = ""): This argument currently serves no purpose - it will become necessary should user authentication be handled by this app (as opposed to ocurring via postman).

- `user_auth_token` (optional, default value = ""): Obtained as part of [User Authentication via Postman](#user-authentication-via-postman). Used to authorise certain actions such as creation/deletion of user-owned playlists.

- `user_refresh_token` (optional, default value = ""): Obtained as part of [User Authentication via Postman](#user-authentication-via-postman). This is used to request a new `user_auth_token` when the old token has expired (see [user_auth_utils()](#user_auth_utils)).

## response_utils

### request_successful()

### error_message()

## client_utils

### read_client_auth_token()

### write_client_auth_token()

### get_client_auth_token()

### return_client_auth_token()

### client_token_expired()

### manage_client_creds()

## user_auth_utils

### read_user_auth_token()

### read_user_refresh_token()

### write_user_auth_token()

### write_user_refresh_token()

### return_user_auth_token()

### user_auth_token_expired()

### get_user_refresh_token()

### user_auth_token_from_refresh_token()

### manage_userauth_creds()

## user_utils

### get_user_info()

### get_user_top_artists()

### user_top_artists_ranked()

### get_user_top_tracks()

### user_top_tracks_ranked()

### get_user_playlists()

## artist_utils

### get_artist()

## track_utils

### get_track_info()

### get_audio_features()

### get_audio_analysis()

### get_recommendations()

## playlist_utils

### playlist_exist()

### get_playlist()

### get_playlist_tracks()

### get_playlist_track_uris()

### get_playlist_artists()

### create_playlist()

### created_playlist_cleanup()

### edit_playlist_details()

### append_tracks_to_playlist()

### remove_tracks_from_playlist()

### find_potential_duplicates()

### append_playlists_to_playlist()

### combine_playlists()

### get_playlist_track_audio_features()

### get_playlist_audio_features()

### get_average_playlist_audio_features()

### playlist_of_recommended_tracks()

### recommend_tracks_from_playlist()
