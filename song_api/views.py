from django.shortcuts import render
from rest_framework.response import Response
from song_api import models
from song_api import serializers
from rest_framework.decorators import api_view
from song_api import spotifyAPI
from song_api import egoNetwork
from django.http import JsonResponse
from song_api import serializers
from typing import List, Dict

# Create your views here.

@api_view(['POST'])
def trackDetails(request) -> Response:
    """
    Retrieve track details and return recommended songs.

    Args: 
        request (Request): The HTTP request object.

    Returns: 
        Response: The HTTP response object containing the recommended songs.

    Raises: 
        models.Song.DoesNotExist: If the requested song does not exist in the database.

    """
    try:
        song = models.Song.objects.get(songName= request.data['search'])
        serializer = serializers.SongSerializer(song)
        recommended_songs = song.recommendedSongs.all().order_by('-popularity')
        recommendation = [s.songName for s in recommended_songs]
        return Response({"Recommended Songs": recommendation})

    
    except models.Song.DoesNotExist:
        spotifyInstance = spotifyAPI.SpotifyAPI(request.data)
        songId, songName, collaboratedArtists, topTracks = spotifyInstance.getSongDetails()

        if topTracks == "Error: No song found with the given name.":
            return Response({"Error": topTracks})
        graph = egoNetwork.ConstructGraph(collaboratedArtists)
        artistNetwork = graph.extractArtists()
        songPopularity = topTracksFromEgoNetwork(artistNetwork, topTracks)
        
        recommendedSongsName = [data['name'] for data in songPopularity][:10]
        recommendedSongsId = [data['id'] for data in songPopularity][:10]
        recommendedSongsPopularity = [data['popularity'] for data in songPopularity][:10]

        song = models.Song.objects.create(songId = songId, songName = songName)
        
        for id, name, songPopularity in zip(recommendedSongsId, recommendedSongsName, recommendedSongsPopularity):
            try: 
                suggestion = models.RecommendedSong.objects.get(songId=id)
            except models.RecommendedSong.DoesNotExist:
                suggestion = models.RecommendedSong.objects.create(songId=id, songName=name, popularity=songPopularity)
                suggestion.save()
            song.recommendedSongs.add(suggestion)

        serializer = serializers.SongSerializer(song)
        recommended_songs = song.recommendedSongs.all().order_by('-popularity')
        recommendation = [s.songName for s in recommended_songs]
        return Response({"Recommended Songs": recommendation})



@api_view(['GET'])
def searchHistory(request) -> Response:
    """
    Retrieve the search history of songs.

    This function retrieves all the songs from the database and returns them as a response.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        Response: The HTTP response object containing the serialized data of all songs.

    """
    allSongs = models.Song.objects.all()
    serializer = serializers.SongSerializer(allSongs, many=True)
    return Response(serializer.data)



def topTracksFromEgoNetwork(artistNetwork: List[str], topTracks: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    """
    Returns a list of recommended tracks based on the artist network and their top tracks.

    Args:
        artistNetwork (List[str]): A list of artists in the network.
        topTracks (Dict[str, List[Dict[str, str]]]): A dictionary containing the top tracks for each artist.

    Returns:
        List[Dict[str, str]]: A list of recommended tracks sorted by popularity.
    """
    songList = []
    for artist in artistNetwork:
        songList.extend(topTracks[artist])

    recommendation = sorted(songList, key=lambda x: x['popularity'], reverse=True)
    return recommendation