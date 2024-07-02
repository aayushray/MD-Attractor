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
    allSongs = models.Song.objects.all()
    serializer = serializers.SongSerializer(allSongs, many=True)
    return Response(serializer.data)

def topTracksFromEgoNetwork(artistNetwork: List[str], topTracks: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    songList = []
    for artist in artistNetwork:
        songList.extend(topTracks[artist])

    recommendation = sorted(songList, key=lambda x: x['popularity'], reverse=True)
    return recommendation