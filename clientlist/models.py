from django.db import models
from member.models import CustomFacebookUser, Client
from playlist.models import Playlist
from music.models import Track

# Playlists on other music services, such as a Spotify playlist
class Clientlist(models.Model):
    '''
    Clientlist
    '''
    client = models.ForeignKey(Client)
    client_unique = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, blank=True)
    client_owner = models.CharField(max_length=255, blank=True)
    follower_count = models.IntegerField(blank=True, null=True) # Spotify
    tuneboss = models.ForeignKey(CustomFacebookUser, related_name="tuneboss_clientlist")
    members = models.ManyToManyField(CustomFacebookUser, related_name="member_clientlists", through='ClientlistFollow')
    playlists = models.ManyToManyField(Playlist)
    tracks = models.ManyToManyField(Track, through='ClientlistTrack')
    url = models.CharField(max_length=255, blank=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode(str(id))

# Tracks on client lists, such as a Spotify playlist
class ClientlistTrack(models.Model):
    '''
    ClientlistTrack
    '''
    clientlist = models.ForeignKey(Clientlist)
    client_unique = models.CharField(max_length=255, null=True, blank=True)
    track = models.ForeignKey(Track)

    added_at = models.DateTimeField()
    added_by = models.CharField(max_length=255, blank=True)
    

# Followers of client lists, such as a Spotify playlist
class ClientlistFollow(models.Model):
    user = models.ForeignKey(CustomFacebookUser)
    clientlist = models.ForeignKey(Clientlist)