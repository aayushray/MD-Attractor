from django.urls import path
from song_api import views

urlpatterns = [
    path('', views.trackDetails, name='home')
]