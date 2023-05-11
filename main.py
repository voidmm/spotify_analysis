import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import cred 
import create_spotify_dataset as csp
from pathlib import Path


if __name__ == "__main__":
    
    #Intantiate the SpotifyOAuth class to authenticate requests
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.client_id, client_secret=cred.client_secret, redirect_uri=cred.redirect_url),requests_timeout=10, retries=10)
    
    #Intantiate the createSpotifyDataset class with 
    spotify = csp.createSpotifyDataset(csv_directory=Path("/csv"), csv_name='tests', spotify_auth=sp, user_id=cred.user)
    
    #get track IDs
    track_ids = spotify.get_track_ids(playlist_id='37i9dQZF1DWWmGB2u14f8m')
    
    #get track features
    track_features = spotify.get_track_features('6kvoHl80mfCVTv7XnZkjQn')
    
    #create playlist dataset
    #playlist = spotify.create_playlist_dataset(playlist_id='37i9dQZF1DX4joPVMjBCAo', playlist_info={'Decade': '1950'})
    
    
    playlists = {'37i9dQZF1DWWmGB2u14f8m': {'Decade': '1950'}}
                                                                
    #create dataset from multiple playlists 
    #spotify.create_dataset(playlists)
    
    #append csv files
    spotify.append_csv_files()
        
    
    
        