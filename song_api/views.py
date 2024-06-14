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

    network = egoNetwork.ConstructGraph(collaboratedArtists)
    return JsonResponse(topTracks, safe=False)