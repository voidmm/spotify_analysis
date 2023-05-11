import pandas as pd
from datetime import datetime
import glob
import os
import time
from pathlib import Path



class createSpotifyDataset():
    
    '''
    A class used to create a Spotify Dataset
    
    Attributes
    ----------
    csv_directory : str
        Directory where you want to save the created csv file
    csv_name : str
        Name of the csv file you want to create
    sp : spotipy.client.Spotify class
        Spotify API Client Endpoint
    user_id : str
        Your spotify user ID
    
    Methods
    ----------
    get_track_ids(playlist_id: str) -> list
        Reads out the track IDs of a Spotify playlist
    get_track_features(track_id: str) -> list
        Reads out the track features of one Spotify track.
    create_playlist_dataset(self, playlist_id: str, playlist_info: str) -> list
        Creates a Dataset from one playlist ID. The Dataset consists of the track audio features and other track information.
    create_dataset(self, playlists: dict) -> None
        Creates a Dataset from multiple playlist IDs, enriched with additional features.
    append_csv_files(self) -> None
       Appends all the csv files in the folder 'APPEND' and saves the resulting file in the csv_directory
       
    '''
   
    def __init__(self, csv_directory: str, csv_name: str, spotify_auth, user_id):
        self.csv_directory = csv_directory
        self.csv_name = csv_name
        self.sp = spotify_auth;
        self.user_id = user_id
        

    def get_track_ids(self, playlist_id: str) -> list:
        
        '''
        Reads out a list of track IDs of a Spotify playlist.
        
        Parameters
        ----------
        playlist_id : str

        Returns
        ----------
        track_ids : list of track IDs as str
        
        '''
        
        track_ids = []
        playlist = self.sp.user_playlist(self.user_id, playlist_id)
            

        for item in playlist['tracks']['items']:
            track = item['track']
            track_ids.append(track['id'])
            
        return track_ids
    
    
    def get_track_features(self, track_id: str) -> list:
        
        '''
        Reads out the track features of one Spotify track.
        
        Audio feature documentation can be found here: 
            https://developer.spotify.com/documentation/web-api/reference/get-several-audio-features
        
        Parameters
        ----------
        track_id : str
          
        Raises
        ------
        TypeError
           If a feature is not available, the track is skipped
           
        Returns
        ----------
        track_ids : list of track features 
        
        '''
        
        track_info = self.sp.track(track_id)
        feature_info = self.sp.audio_features(track_id)
        
        try:
            name = track_info['name']
            album = track_info['album']['name']
            artist = track_info['album']['artists'][0]['name']
            release_date = track_info['album']['release_date']
            length = track_info['duration_ms']
            popularity = track_info['popularity']
            acousticness = feature_info[0]['acousticness']
            danceablity = feature_info[0]['danceability']
            energy = feature_info[0]['energy']
            instrumentalness = feature_info[0]['instrumentalness']
            liveness = feature_info[0]['liveness']
            loudness = feature_info[0]['loudness']
            speechiness = feature_info[0]['speechiness']
            tempo = feature_info[0]['tempo']
            time_signature = feature_info[0]['time_signature']
            valence = feature_info[0]['valence']
    
            track_data = [track_id, name, album, artist, release_date, length, popularity, acousticness, danceablity, energy, instrumentalness, liveness, loudness, speechiness, tempo, time_signature, valence]
            return track_data
        
        except TypeError:
            print('TypeError for: ' + str(name) + ' ' + str(artist) + '. Skipping this track.')
            return None
                
    
    def create_playlist_dataset(self, playlist_id: str, playlist_info: dict) -> list:
        
        '''
        Creates a Dataset from one playlist ID. The Dataset consists of the track audio features and other track information.
        
        Parameters
        ----------
        playlist_id : str
        playlist_info : dict ( example: {'Decade': '1970', 'Year':   '1971'} )
          
        Raises
        ------
        TypeError
           If a feature is not available, the track is skipped
           
        Returns
        ----------
        track_ids : list of track features 
        
        '''
        try:
            #Use the keys of the dictionary containing the playlist information as the column names of the additional featurein the dataset
            playlist_column_name = [k for k in sorted(playlist_info.keys())]
            
            #The values of the dictionary containing the playlist information are the additional feature value that is passed
            playlist_feature =  [v for v in sorted(playlist_info.values())]
        except (TypeError, AttributeError):
                raise Exception('\n' + 
                                'Playlist features format invalid. Please make sure to pass the playlist features as a dictionary. Example:' + 
                                '\n' + {'37i9dQZF1DX0fr2A59qlzT': {'Decade': '1970', 'Year':   '1971'}} + '\n')
        
        #Check if the keys and values of the dictionary containing the playlist information consist of allowed data types string, float and int
        if  all ([isinstance(a, (str,float,int)) for a in playlist_column_name + playlist_feature]):
            
            #If so, proceed with processing the playlist
            print('Parsing playlist: '+ str(playlist_id) + '\n')
            
        #If either the keys or the values are empty, it means we either are missing the column name or the feature itself.
        #In that case skip the feature addition alltogether
        elif (len(playlist_info) == 0 or len(playlist_column_name) == 0):
            print('Playlist features incomplete. Dataset will be created without additional playlist features.' + '\n')
            playlist_column_name = []
            playlist_feature = []
            
        #If an invalid data type is passed as the feature, we will also not consider the additional feature
        else: 
            print('Parsing playlist: '+ str(playlist_id) + '\n')
            print('No additional playlist features passed for: ' + playlist_id + '\n')
            playlist_column_name = []
            playlist_feature = []
     
        #In this block, the track IDs of each track of the playlist are extracted
        track_ids = self.get_track_ids(playlist_id)
        track_list = []
        
        for track_id in track_ids:
            time.sleep(.3)
            track_data = self.get_track_features(track_id)
            
            if track_data:
                track_list.append(track_data + playlist_feature)
            else:
                pass
        
        #The playlist is transformed into a pandas Dataframe
        playlist = pd.DataFrame(track_list, columns = ['Track ID', 'Name', 'Album', 'Artist', 'Release Date', 'Length', 'Popularity', 'Acousticness', 'Danceability', 'Energy', 'Instrumentalness',
                                                       'Liveness', 'Loudness', 'Speechiness', 'Tempo', 'Time Signature', 'Valence'] + playlist_column_name)
        print(playlist.head(5))
        
        return playlist
        
    
    def create_dataset(self, playlists: dict) -> None:
        
        '''
        Creates a Dataset from multiple playlist IDs, enriched with the features passed additionally.
        
        Parameters
        ----------
        playlists :  dict ( example: { '37i9dQZF1DWXbLOeOIhbc5': {'Decade': '1980',
                                                         'Year':   '1980'} )
          
        Raises
        ------
        OSError
           If an incorrect directory is passed, the dataset will not be created
           
        Returns
        ----------
        None
        
        csv file is saved to csv_directory

        '''
        playlist_dataset = []
        playlist_ids = []
        
        #First, ceck if the directory where the resulting dataset is supposed to be saved is valid
        try:
            os.chdir(self.csv_directory)
            print('Dataset will be saved in: ' + str(self.csv_directory))
        except OSError:
            raise OSError('Directory does not exist. Please pass a valid directory.' + '\n')
        
        #For every Paylist ID that was not yet parsed, parse it and create a dataset
        for playlist_id, playlist_info in playlists.items():
            if playlist_id not in playlist_ids:
                
                print('\n' + 'Creating dataset.' + '\n')
                
                playlist = self.create_playlist_dataset(playlist_id, playlist_info)
                playlist_dataset.append(playlist)
                playlist_ids.append(playlist_id)
                time.sleep(5)
            else:
                pass
        
        #Concatinate all playlists and drop duplicate tracks
        playlist_dataset = pd.concat(playlist_dataset)
        playlist_dataset = pd.DataFrame.drop_duplicates(playlist_dataset,subset=['Name', 'Artist'])
        playlist_dataset.to_csv(str(self.csv_directory) + '/' + self.csv_name + '.csv', mode='w+')
            
        print('Dataset successfully created.')
        
        return None
      

    
    def append_csv_files(self) -> None:
        
        '''
        Appends all the csv files in the folder 'APPEND' and saves the resulting file in the csv_directory. 
        
        The 'APPEND' folder will be created if it is not present and must contain the respective .csv files that are supposed to be concatenated.
        
        Parameters
        ----------
        
        Raises
        ------
        FileNotFoundError
           If an invalid directory was passed, the csv files cannot be concatenanted
        
        ValueError
           If there are no csv files in the APPEND folder, a prompt will ask for the insertion of csv files
           
        Returns
        ----------
        None
        
        Appended csv file is saved to csv_directory

        '''
        
        append_folder = Path(str(self.csv_directory) + '/APPEND')
        
        
        try:
            #Check if the 'APPEND' folder exists and create it if not
            isExist = os.path.exists(append_folder)
            if not isExist:
                os.makedirs(append_folder)
                print('Please check directory: ' + str(self.csv_directory) + '/APPEND' + 'and copy the csv files to be appended there.' + '\n')
            
            #Find all .csv files in the APPEND folder and copy their names inside csv_files
            os.chdir(append_folder)
            csv_files = glob.glob('*.{}'.format('csv'))
            
            #Build a datetime string that is appended to the csv file name so that files aren't overwritten
            now = str(datetime.now())
            now = ' ' + now.split('.',1)[0].replace(':', '_').replace('-','_')
            
            playlist_dataset = []
            
            #Append the datasets
            for dataset in csv_files:
                    dataset_df = pd.read_csv(dataset)
                    playlist_dataset.append(dataset_df)
            
            #Concatenate the separate datasets and drop duplicates if there are any. Save to a csv file
            playlist_dataset = pd.concat(playlist_dataset, ignore_index=True)
            playlist_dataset = pd.DataFrame.drop_duplicates(playlist_dataset,subset=['Name', 'Artist'])
            playlist_dataset.to_csv(str(self.csv_directory) + '/' + self.csv_name + now + '.csv')
            
            print('\n' + str(self.csv_directory) + '/' + self.csv_name + now + '.csv' +' created' + '\n')
            
        except FileNotFoundError:
            raise FileNotFoundError('Please check the directory and make sure a valid directory was passed.')
        except ValueError:
            raise ValueError('No .csv files found in ' + str(append_folder) + '. Please insert .csv files for concatentation.')
        
        return None
        
        
        
    
    
            
        
            
            
            
        
 
        
        
        
    
    
        