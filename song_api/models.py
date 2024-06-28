from django.db import models

class Song(models.Model):
    songId = models.CharField(max_length=100, primary_key=True)
    songName = models.CharField(max_length=100)
    recommendedSongs = models.ManyToManyField('RecommendedSong')

    def __str__(self):
        return self.songName
    
class RecommendedSong(models.Model):
    songId = models.CharField(max_length=100, primary_key=True)
    songName = models.CharField(max_length=100)
    popularity = models.IntegerField(default=0)

    def __str__(self):
        return self.songId