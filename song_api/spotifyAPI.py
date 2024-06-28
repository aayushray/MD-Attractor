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
        trackName = self.data['search']
        results = self.sp.search(q='track:' + trackName, type='track')

        if not len(results['tracks']['items']):
            return None, None, None, "Error: No song found with the given name."

        self.songId = results['tracks']['items'][0]['id']
        self.songName = results['tracks']['items'][0]['name']

        self.artistDetails = results['tracks']['items'][0]['artists']
        self.artistID = self.artistDetails[0]['id']

        # Fetching the Genre of the Song
        self.genres = self.collectGenres(self.artistID)

        # List of Artists, who had collaborated with the Primary artist
        self.collaboratedArtists = self.relatedArtists(self.artistID, self.genres)

        # for artists in self.collaboratedArtists:
        self.topTracks = self.getTopTracks(self.collaboratedArtists)

        return self.songId, self.songName, self.collaboratedArtists, self.topTracks


    def collectGenres(self, artistID):
        result = self.sp.artist(artistID)
        genres = result['genres']

        return genres
    

    def relatedArtists(self, artistID, genres):
        collaborations = {artistID: genres}
        results = self.sp.artist_related_artists(artist_id = artistID)
        items = results['artists']

        for artist in items:
            collaborations[artist['id']] = artist['genres']

        return collaborations
    
    def getTopTracks(self, collaboratedArtists):
        topTracks = {}
        for artistID in collaboratedArtists:
            results = self.sp.artist_top_tracks(artist_id = artistID)
            currentArtistTopTracks = []
            for trackNumber in range(0, len(results['tracks'])):
                trackInfo = {
                    'name': results['tracks'][trackNumber]['name'],
                    'id': results['tracks'][trackNumber]['id'],
                    'popularity': results['tracks'][trackNumber]['popularity']
                }
                currentArtistTopTracks.append(trackInfo)

            topTracks[artistID] = currentArtistTopTracks
        return topTracks
