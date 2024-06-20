from django.shortcuts import render
from rest_framework.response import Response
from song_api import models
from song_api import serializers
from rest_framework.decorators import api_view
from song_api import spotifyAPI
from song_api import egoNetwork
from django.http import JsonResponse

# Create your views here.

@api_view(['POST'])
def trackDetails(request):
    spotifyInstance = spotifyAPI.SpotifyAPI(request.data)
    collaboratedArtists, topTracks = spotifyInstance.getSongDetails()

    graph = egoNetwork.ConstructGraph(collaboratedArtists)
    artistNetwork = graph.extractArtists()
    songPopularity = topTracksFromEgoNetwork(artistNetwork, topTracks)
    print(songPopularity)
    recommendedSongs = [data[0] for data in songPopularity]

    return JsonResponse(recommendedSongs, safe=False)

def topTracksFromEgoNetwork(artistNetwork, topTracks):
    songList = []
    for artist in artistNetwork:
        songList.append(topTracks[artist])

    flat_list = [item for sublist in songList for item in sublist]
    pairs = [(k, v) for d in flat_list for k, v in d.items()]
    recommendation = sorted(pairs, key=lambda x: x[1], reverse=True)
    return recommendation