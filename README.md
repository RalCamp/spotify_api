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

- `user_id` (optional, default value = ""): The id associated with your user - required for [create_playlist()](#create_playlist) and [get_user_playlists()](#get_user_playlistsuser_owned_onlytrue-print_resultsfalse). This id is not currently recovered automatically, but can be found using [get_user_info()](#get_user_info).

- `user_auth_code` (optional, default value = ""): This argument currently serves no purpose - it will become necessary should user authentication be handled by this app (as opposed to ocurring via postman).

- `user_auth_token` (optional, default value = ""): Obtained as part of [User Authentication via Postman](#user-authentication-via-postman). Used to authorise certain actions such as creation/deletion of user-owned playlists.

- `user_refresh_token` (optional, default value = ""): Obtained as part of [User Authentication via Postman](#user-authentication-via-postman). This is used to request a new `user_auth_token` when the old token has expired (see [user_auth_utils()](#user_auth_utils)).

## response_utils

Handles responses to http requests, using the python `requests` package.

### request_successful(response_object)

Determines whether or not a request has been successful.

### error_message(response_object)

Provides the status code and additional information about the response object in the case of a request failure.

## client_utils

Handles actions related to client authorisation. The `Client` class takes the following arguments: `app_name`, `client_id`, `client_secret` and `client_auth_token`.

### read_client_auth_token()

Reads the client authorisation token from the app's .json file and uses it to update the value of `self.client_auth_token`.

### write_client_auth_token()

Writes the current value of `self.client_auth_token` to the app's .json file.

### get_client_auth_token()

Retrieves `client_auth_token` from Spotify, and writes it to the app's .json file.

### return_client_auth_token()

Returns the client authorisation token. Used in [playlist_utils](#playlist_utils).

### client_token_expired()

Uses a request to one of the example playlists in the Spotify API documentation to check whether or not the client auth token in the app's .json file is valid or not.

### manage_client_creds()

Checks the validity of the current client auth token and requests a new on if the current one has expired.

## user_auth_utils

Handles actions related to user authorisation, specifically `user_auth_token` and `user_refresh_token`. The `UserAuth` class takes the following arguments: `app_name`, `user_auth_token`, `user_refresh_token`, `client_id` and `client_secret`.

### read_user_auth_token()

Reads the user authorisation token from the app's .json file and uses it to update the value of `self.user_auth_token`.

### read_user_refresh_token()

Reads the user refresh token from the app's .json file and uses it to update the value of `self.user_refresh_token`.

### write_user_auth_token()

Writes the current value of `self.user_auth_token` to the app's .json file.

### write_user_refresh_token()

Writes the current value of `self.user_refresh_token` to the app's .json file.

### return_user_auth_token()

Returns the current user authorisation token.

### user_auth_token_expired()

Uses a request to <https://api.spotify.com/v1/me> to determine whether or not the current user authorisation token has expired.

### get_user_refresh_token()

Requests a new user refresh token from the API.

### user_auth_token_from_refresh_token()

Uses the user refresh token to request a new user authorisation token.

### manage_userauth_creds()

Checks the validity of the current user authorisation token, and requests a new one if it has expired.

## user_utils

Gets information about the current user, including user id, top tracks and top artists. The `User` class takes the arguments `user_id` and `userauth` where `userauth` is an instance of the `UserAuth` class.

### get_user_info()

Returns a .json containing information about the current user including display name, id, and information about followers. More information can be returned by increasing the [scope granted to the app by the user](#user-authentication-via-postman). More information about the http request that this function uses can be found [here](https://developer.spotify.com/documentation/web-api/reference/get-current-users-profile).

### get_user_top_artists(time_range)

Returns a .json of the user's top artists within a given time range. The accepted values for `time_range` are:

- `'long_term'`: ~1 year

- `'medium_term'`: ~6 months

- `'short_term'`: ~4 weeks

More information about the http request that this function uses can be found [here](https://developer.spotify.com/documentation/web-api/reference/get-users-top-artists-and-tracks). Note that while the 'default' request can only return a maximum of 50 items at a time, the function is written to retun *all* items.

### user_top_artists_ranked(time_range, print_results=False)

Uses [get_user_info()](#get_user_info) to generate a dictionary of the user's top artists, along with their rankings. These rankings can be printed to the terminal by setting `print_results` to `True`.

### get_user_top_tracks(time_range)

Returns a .json of the user's top tracks within a given time range. The accepted values for `time_range` are:

- `'long_term'`: ~1 year

- `'medium_term'`: ~6 months

- `'short_term'`: ~4 weeks

More information about the http request that this function uses can be found [here](https://developer.spotify.com/documentation/web-api/reference/get-users-top-artists-and-tracks). Note that while the 'default' request can only return a maximum of 50 items at a time, the function is written to retun *all* items.

### user_top_tracks_ranked(time_range, print_results=False, range=0)

Uses [get_user_top_tracks()](#get_user_top_trackstime_range) to generate a dictionary of the user's top tracks, along with their rankings. These rankings can be printed to the terminal by setting `print_results` to `True`. The function will return all of the users top artists unless `range` is set to an integer value greater than 0, in which case it will return up to that many results (if `range` is set to a value greater than the total number of results the function will simply return all the results).

### get_user_playlists(user_owned_only=True, print_results=False)

Returns a dictionary of the uris and names of the playlists in the user's library. The default value of `user_owned_only` will cause the function to only return playlists that the user owns - this can be expanded to all playlists in the user's library by setting `user_owned_only` to `True`.

More information about the http request that this function uses can be found [here](https://developer.spotify.com/documentation/web-api/reference/get-list-users-playlists). Note that while the 'default' request can only return a maximum of 50 items at a time, the function is written to retun *all* items.

## artist_utils

Gets information about artists. The `Artist` class takes an instance of the `Client` object as an argument.

### get_artist(artist_id)

Returns a .json containing information about the artist, such as the artist's name, what genres they are associated with and how many followers they have.

More information about the http request that this function uses can be found [here](https://developer.spotify.com/documentation/web-api/reference/get-an-artist).

## track_utils

Gets information about tracks, inclding audio features and analysis, as well as generating recommendations. The `Track` class takes instances of the `Client` and `UserAuth` classes as arguments.

### get_track_info(track_id)

Returns a .json containing information about the track, including album/artist information, track name, track duration and track popularity.

More information about the http request that this function uses can be found [here](https://developer.spotify.com/documentation/web-api/reference/get-track).

### get_audio_features(track_id)

Returns a .json containing a track's audio features. The features measured are as follows:

- **acousticness:** A measure of confidence in the track being acoustic. `1.0` indicates a high confidence.

- **danceability:** A measure of how suitable the track is for dancing. `1.0` is the most danceable.

- **duration_ms:** The duration of the track in milliseconds.

- **energy:** A measure of how "intense" and "active" a track is percieved to be. `1.0` indicates a very high energy.

- **instrumentalness:** A measure of confidence in whether or not the track contains vocal content. A track can be considered instrumental if its instrumentalness is greater than `0.5`, with higher values indicating a greater confidence that the track is instrumental.

- **key:** The key the track is in. `0` is C and each successive integer represents the next semitone up. Returns `-1` if a key cannot be identified.

- **liveness:** A measure of confidence in whether or not the track was performed live. Tracks with a liveness of `0.8` or more can be considered to have been performed live.

- **loudness:** The average loudness of a track in decibels.

- **mode:** Indicates whether the track is in a major (`1.0`) or minor (`0`) key.

- **speechiness:** A measure of how much of the track is spoken word. Values greater than `0.66` indicate that a track is likely entirely spoken word and values below `0.33` indicate that a track contains mostly music or other non-speech sounds.

- **tempo:** The estimated tempo of the track in BPM.

- **time_signature:** The estimated time signature of the track. Ranges from `3` (3/4) to `7` (7/4).

More information about the http request that this function uses can be found [here](https://developer.spotify.com/documentation/web-api/reference/get-audio-features).

### get_audio_analysis(track_id)

Returns a .json contatining a low-level audio analysis of the track, including attempts to calculate position and length of track subdivisions. This function returns a large volume of data which is broadly split into the following categories:

- **metadata:** This includes information such as the timestamp of the analysis and the version of the analyser used.

- **track:** Information about the track as a whole, including the number of samples, loudness, tempo and key.

- **bars:** An array of objects containing the start and duration of each bar, along with a confidence measure for those values.

- **beats:** An array of objects containing the start and duration of each beat, along with a confidence measure for those values.

- **sections:** An array of objects for each distinct section in the track including information on duration, loudness, key, mode and time signature.

- **segments:** An array of objects representing sections of the track that have a roughly consistent sound throughout including information on duration, loudness, timbre and the prevalence of certain pitches.

- **tatums:** As the onomatopoeia suggests, a tatum is the slowest pulse inferred by a listener. This key is an array of each tatum with information about its duration.

More information about the http request that this function uses can be found [here](https://developer.spotify.com/documentation/web-api/reference/get-audio-analysis).

### get_recommendations(limit=20, market=None, seeds={ 'seed_artists': [], 'seed_genres': [], 'seed_tracks': [] }, audio_features=None)

Returns a .json of recommended tracks based on seeds, along with the option to further restirct results by audio values. A maximum of 5 seeds can be provided in any combination, but at least 1 seed **must** be provided. The format of each argument is as folows

- **limit:** *integer* - the target number of recommended tracks. Note that it may not be possible to return the requested number of recommended tracks.

- **market:** *string* - a [two letter country code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) for the market the returned tracks are available in. Defaults to the user's market if left unspecified.

- **seeds:** *dictionary* - the seeds for track recommendation. The values of `seed_artists` and `seed_tracks` are an array of uris, while `seed_genres` is an array of genres.

- **audio_features:** *dictionary* - optional minimum, maximum and target audio feature values to restrict results by. Keys are any of the features discussed in [get_audio_features()](#get_audio_featurestrack_id) prefaced with either `min_`, `max_`, or `target_`.

More information about the http request that this function uses can be found [here](https://developer.spotify.com/documentation/web-api/reference/get-recommendations).

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
