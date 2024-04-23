from datetime import datetime

class Custom():
    def __init__(self, playlist):
        self.playlist = playlist
        
    def manage_democracy_bois_playlist(self, monthly_playlist, archive):
        current_month = datetime.now().strftime('%m/%y')
        playlist_month = (self.playlist.get_playlist(monthly_playlist)['name'])[-5::]
        print("Checking whether playlist needs archiving...")
        if current_month != playlist_month:
            playlist_tracks = self.playlist.get_playlist_track_uris(monthly_playlist)
            new_name = f"Democracy Sharing {current_month}"
            print("Moving tracks to archive...")
            self.playlist.append_tracks_to_playlist(archive, playlist_tracks)
            print("Clearing monthly playlist...")
            self.playlist.remove_tracks_from_playlist(monthly_playlist, playlist_tracks)
            print("Renaming monthly playlist...")
            self.playlist.edit_playlist_details(monthly_playlist, new_title=new_name)
            print("Complete\n")
        else:
            print("The playlist is not yet out of date\n")