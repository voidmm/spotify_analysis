Spotify Analysis with spotipy and plotly
=========
Spotify provides a Web API: https://developer.spotify.com/documentation/web-api making it possible to analyze metadeta among providing many other functionalities. To perform the analysis in Python, spotipy was used to collect data over the Spotify API.

The aim of this analysis was to 
1. Create a dataset from Spotify playlists that contain the most popular tracks of each decade, starting from the 1950s
2. Extract the audio features of these tracks
3. Showcase and analyze the decade-specific music trends with Python Plotly

Spotify API credentials
---------
To use the Spotify API, you will need to authorize yourself and of course be an active Spotify user with a respective User ID. Spotipy makes it pretty easy with its Authorization Code flow. You can set your credentials as environment variables or set them in a separate python file. 
The necessary authorization parameters you will need to set are the following:

client_id=''
client_secret=''
redirect_url=''
user=''

Please adjust it in the cred.py file and checkout spotipys documentation: https://spotipy.readthedocs.io/en/2.6.3/#authorization-code-flow
for the authorization code flow.

Build the Dataset
---------
With the create_spotify_dataset module you can collect Spotify track audio feature data by passing a public playlist ID.

Example:

    #Intantiate the SpotifyOAuth class to authenticate requests
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.client_id, client_secret=cred.client_secret, redirect_uri=cred.redirect_url),requests_timeout=10, retries=10)
    
    #Intantiate the createSpotifyDataset class with 
    spotify = 
    csp.createSpotifyDataset(
        csv_directory=Path("<path-where-the-resulting-csv-file-should-be-saved-to>"), csv_name='<name-of-csv-file>', spotify_auth=sp, user_id=cred.user)
	
    playlists = {'37i9dQZF1DWSV3Tk4GO2fq': {'Decade': '1950'}}
                                                                
    #create dataset from playlist 
    spotify.create_dataset(playlists)

See more examples in main.py

More information about track audio features: https://developer.spotify.com/documentation/web-api/reference/get-audio-features
More information about spotipy: https://spotipy.readthedocs.io/en/2.22.1/?highlight=user_playlist#

Leverage Spotify playlists
---------
By manually adding features to each Playlist ID, you can greatly enhance the richness of the dataset.
While some of the features (e.g. genres) can be collected with the Spotify API with other functions, introducting an additional
dimension allows you to analyze the characteristics of the catalogue on an even borader spectrum.

In the example analysis, the audio features categorized by decades were analyzed. You could also analyze:
- Your music taste vs. a friends by comparing your Spotify Best of playlists
- Bands by comparing the "This is" playlist Spotify curates
- Chart playlists of different countries

Appending csv files
---------
There is a small helper function called append_csv_files() as part of the createSpotifyDataset class that allows you to append the csv files that are inside the 'APPEND' folder. Due to regular request timeouts, it might happen that multiple runs have to be started (and multiple datasets created), which is where this function comes in.

    #append csv files
    spotify.append_csv_files()

Dataset specifications
---------
The dataset consisting of audio track features with the additional decade feature is part of this Project and can be downloaded for a subsequent analysis (check the "csv" folder).

spotify_decades_dataset: Is the original dataset that was created and can be found in the csv folder, listing all parsed track information
year_features: Is the aggregated dataset that contains the mean and standard deviation of each year, beginning at 1970 (no year-specific playlist are available for years prior to that)

Analyze the dataset with Plotly
---------
The Plotly analysis was done in a Jupyter Notebook and is supposed to offer an example of how plotly can be leveraged to analyze Spotify audio features.


