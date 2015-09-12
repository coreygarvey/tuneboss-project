from django.db import models
from member.models import CustomFacebookUser, Client
from music.models import Track, Artist

# TuneBoss Playlists
class Playlist(models.Model):
		'''
		Playlist
		'''
		display_name = models.CharField(max_length=255, blank=True)
		tuneboss = models.ForeignKey(CustomFacebookUser, related_name="tuneboss_playlist")
		members = models.ManyToManyField(CustomFacebookUser, related_name="member_playlist", through='PlaylistFollow')
		tracks = models.ManyToManyField(Track, through='PlaylistTrack')
		picture = models.ImageField()
		description = models.CharField(max_length=255, blank=True,)
		#keywords = ArrayField/ManyToMany
		keyword_variety = models.DecimalField(max_digits=5, decimal_places=2)
		year = models.DecimalField(max_digits=5, decimal_places=2)
		year_variety = models.DecimalField(max_digits=5, decimal_places=2)
		tempo = models.DecimalField(max_digits=5, decimal_places=2)
		tempo_variety = models.DecimalField(max_digits=5, decimal_places=2)
		#genre = ArrayField/ManyToMany
		genre_variety = models.DecimalField(max_digits=5, decimal_places=2)
		hottness = models.DecimalField(max_digits=5, decimal_places=2)
		hottness_variety = models.DecimalField(max_digits=5, decimal_places=2)
		familiarity = models.DecimalField(max_digits=5, decimal_places=2)
		similarity = models.DecimalField(max_digits=5, decimal_places=2)
				# 0, no artists connected, 1, all artists connected to all other artists
		artists = models.ManyToManyField(Artist)
    
# Tracks on Tuneboos Playlists
class PlaylistTrack(models.Model):
		'''
		PlaylistTrack
    '''
		playlist = models.ForeignKey(Playlist)
		track = models.ForeignKey(Track)
		added_at = models.DateTimeField()
		added_by = models.DateTimeField()

# Followers of Tuneboss Playlists
class PlaylistFollow(models.Model):
		user = models.ForeignKey(CustomFacebookUser)
		playlist = models.ForeignKey(Playlist)