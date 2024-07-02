import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
from typing import Dict, List, Optional, Tuple

load_dotenv()

class SpotifyAPI():
    def __init__(self, data: Dict[str, str]):
        self.client_id: str = os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret: str = os.getenv('SPOTIFY_CLIENT_SECRET')
        self.sp: spotipy.Spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=self.client_id,client_secret=self.client_secret))
        self.data: Dict[str, str] = data

    def getSongDetails(self) -> Tuple[Optional[str], Optional[str], Optional[Dict[str, List[str]]], Optional[Dict[str, List[Dict[str, str]]]]]:
        trackName: str = self.data['search']
        results: Dict[str, Dict[str, List[Dict[str, str]]]] = self.sp.search(q='track:' + trackName, type='track')

        if not len(results['tracks']['items']):
            return None, None, None, "Error: No song found with the given name."

        self.songId: str = results['tracks']['items'][0]['id']
        self.songName: str = results['tracks']['items'][0]['name']

        self.artistDetails: List[Dict[str, str]] = results['tracks']['items'][0]['artists']
        self.artistID: str = self.artistDetails[0]['id']

        # Fetching the Genre of the Song
        self.genres: List[str] = self.collectGenres(self.artistID)

        # List of Artists, who had collaborated with the Primary artist
        self.collaboratedArtists: Dict[str, List[str]] = self.relatedArtists(self.artistID, self.genres)

        # for artists in self.collaboratedArtists:
        self.topTracks: Dict[str, List[Dict[str, str]]] = self.getTopTracks(self.collaboratedArtists)

        return self.songId, self.songName, self.collaboratedArtists, self.topTracks


    def collectGenres(self, artistID: str) -> List[str]:
        result: Dict[str, List[str]] = self.sp.artist(artistID)
        genres: List[str] = result['genres']

        return genres
    

    def relatedArtists(self, artistID: str, genres: List[str]) -> Dict[str, List[str]]:
        collaborations: Dict[str, List[str]] = {artistID: genres}
        results: Dict[str, List[Dict[str, str]]] = self.sp.artist_related_artists(artist_id = artistID)
        items: List[Dict[str, str]] = results['artists']

        for artist in items:
            collaborations[artist['id']] = artist['genres']

        return collaborations
    
    def getTopTracks(self, collaboratedArtists: Dict[str, List[str]]) -> Dict[str, List[Dict[str, str]]]:
        topTracks: Dict[str, List[Dict[str, str]]] = {}
        for artistID in collaboratedArtists:
            results: Dict[str, List[Dict[str, str]]] = self.sp.artist_top_tracks(artist_id = artistID)
            currentArtistTopTracks: List[Dict[str, str]] = []
            for trackNumber in range(0, len(results['tracks'])):
                trackInfo: Dict[str, str] = {
                    'name': results['tracks'][trackNumber]['name'],
                    'id': results['tracks'][trackNumber]['id'],
                    'popularity': results['tracks'][trackNumber]['popularity']
                }
                currentArtistTopTracks.append(trackInfo)

            topTracks[artistID] = currentArtistTopTracks
        return topTracks
