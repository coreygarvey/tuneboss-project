from django.db import models
from member.models import CustomFacebookUser, Client


# Spotify Albums
class Album(models.Model):
    '''
    Albums
    '''
    client = models.ForeignKey(Client)
    client_unique = models.CharField(max_length=255, blank=True)
    uri = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255, blank=True)
    href = models.URLField(max_length=255)
    popularity = models.DecimalField(max_digits=5, decimal_places = 2)
    release_date = models.DateField()
    image_url = models.URLField(null=True, blank=True)
    image_width = models.IntegerField(null=True, blank=True)
    image_height = models.IntegerField(null=True, blank=True)

# Spotify Artists
class Artist(models.Model):
    '''
    Artists
    '''
    client = models.ForeignKey(Client)
    client_unique = models.CharField(max_length=255, blank=True)
    en_unique = models.CharField(max_length=255, null=True, blank=True)
    uri = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255, blank=True)
    href = models.URLField(max_length=255)
    popularity = models.IntegerField(null=True, blank=True) #Spotify
    followers = models.IntegerField(null=True, blank=True) #Spotify
    #genres = 
    #terms = 
    hottness = models.DecimalField(max_digits=5, decimal_places = 2, null=True, blank=True)
    familiarity = models.DecimalField(max_digits=5, decimal_places = 2, null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    image_width = models.IntegerField(null=True, blank=True)
    image_height = models.IntegerField(null=True, blank=True)
    albums = models.ManyToManyField(Album, null=True, blank=True)
    

# Spotify Tracks
class Track(models.Model):
    '''
    Tracks
    '''
    client = models.ForeignKey(Client, null=True, blank=True)
    client_unique = models.CharField(max_length=255, null=True, blank=True)
    en_unique = models.CharField(max_length=255, null=True, blank=True)
    uri = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    artist_name = models.CharField(max_length=255, null=True, blank=True)
    tb_code = models.CharField(max_length=255, null=True, blank=True)
    tempo = models.DecimalField(max_digits=5, decimal_places = 2, null=True, blank=True)
    energy = models.DecimalField(max_digits=5, decimal_places = 2, null=True, blank=True)
    loudness = models.DecimalField(max_digits=5, decimal_places = 2, null=True, blank=True)
    danceability = models.DecimalField(max_digits=5, decimal_places = 2, null=True, blank=True)
    speechiness = models.DecimalField(max_digits=5, decimal_places = 2, null=True, blank=True)
    acousticness = models.DecimalField(max_digits=5, decimal_places = 2, null=True, blank=True)
    liveness = models.DecimalField(max_digits=5, decimal_places = 2, null=True, blank=True)
    instrumentalness = models.DecimalField(max_digits=5, decimal_places = 2, null=True, blank=True)
    key = models.DecimalField(max_digits=5, decimal_places = 2, null=True, blank=True)
    duration = models.DecimalField(max_digits=5, decimal_places = 2, null=True, blank=True)
    image = models.URLField(null=True, blank=True)
    album = models.ForeignKey(Album, null=True, blank=True)
    artists = models.ManyToManyField(Artist, null=True, blank=True)


# Genres
class Genre(models.Model):
    '''
    Genres
    '''
    name = models.CharField(max_length=255, blank=True)

# Terms
class Term(models.Model):
    '''
    Terms
    '''
    name = models.CharField(max_length=255, blank=True)