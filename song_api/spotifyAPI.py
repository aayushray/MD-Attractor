import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()

class SpotifyAPI():
    def __init__(self, data):
        self.client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        self.sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=self.client_id,client_secret=self.client_secret))
        self.data = data

    def getSongDetails(self):
        trackName = self.data['Track Name']
        results = self.sp.search(q='track:' + trackName, type='track')
        self.artistDetails = results['tracks']['items'][0]['artists']
        self.artistID = self.artistDetails[0]['id']

        self.genres = self.collectGenres(self.artistID)
        print(self.genres)

        self.collaboratedArtists = self.relatedArtists(self.artistID, self.genres)
        print(self.collaboratedArtists)

        return self.collaboratedArtists


    def collectGenres(self, artistID):
        result = self.sp.artist(artistID)
        genres = result['genres']

        return genres
    

    def relatedArtists(self, artistID, genres):
        collaborations = [(artistID, genres)]
        results = self.sp.artist_related_artists(artist_id = artistID)
        items = results['artists']

        for artist in items:
            collaborations.append((artist['id'], artist['genres']))

        return collaborations
