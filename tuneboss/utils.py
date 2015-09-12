# shows a user's playlists (need to be authenticated via oauth)

import pprint
import sys
import os
import subprocess

import spotipy
from open_facebook import OpenFacebook
import spotipy.util as util
import requests
import json
import datetime
import math
from django.utils import timezone
from member.models import Client
from clientlist.models import Clientlist, ClientlistTrack, ClientlistFollow
from music.models import Album, Artist, Track

from dateutil.parser import parse as parse_date


def get_playlists(client, username, request):

    if len(username) > 1:
        username = username
    else:
        print "Whoops, need your username!"
        print "usage: python user_playlists.py [username]"
        sys.exit()

    token = util.prompt_for_user_token(username)

    if token:
        
        sp = spotipy.Spotify(auth=token)
        
        playlists = sp.user_playlists(username)
        print playlists
        #playlist = sp.user_playlist(username, playlist_id=playlist, fields=None)
        #print playlist
        #print playlist['tracks']['total']
        limit = 100
        #playlist = sp.user_playlist_tracks(username, playlist_id=playlist, fields=None, limit=limit, offset=100)
        #print playlist
        #print playlist['next']
        i=1
        print "Access Token:"
        me = request.user
        print me
        #graph = get_persistent_graph(user2)
        graph = me.get_offline_graph()
        print graph
        access_token = me.access_token
        print access_token
        facebook = OpenFacebook(access_token)
        me = facebook.get('me', fields ='third_party_id')
        print me
        print 'got it!'
        '''
        for track in playlist['items']:
            print str(i) + ' ' + track['track']['name'] + ' ' + track['track']['uri']
            if i == limit:
                print playlist['next']
                
                
                
                return
            i += 1
        '''

    else:
        print "Can't get token for", username


def get_echonest():
    r = requests.get("http://developer.echonest.com/api/v4/song/search?api_key=MIFPIXGEUZDLAYXMO&format=json&results=1&artist=radiohead&title=karma%20police&bucket=id:spotify&bucket=audio_summary&limit=true")
    s = requests.get("http://developer.echonest.com/api/v4/song/profile?api_key=MIFPIXGEUZDLAYXMO&format=json&track_id=spotify:track:2CYhKfcgrxziIkBLs8cPd0&track_id=spotify:track:1iw4yy8dDH9TcSEcOEWVnO&bucket=audio_summary")
    data = r.json()
    #return data['response']['songs'][0]['audio_summary']['tempo']
    return s.json()




def update_user_playlists(client, username, request):
    current_user = request.user

    if len(username) > 1:
        username = username
    else:
        print "Whoops, need your username!"
        print "usage: python user_playlists.py [username]"
        sys.exit()

    token = util.prompt_for_user_token(username)

    if token:
        sp = spotipy.Spotify(auth=token)
        playlists = sp.user_playlists(username)
        associated_playlists = playlists['items']
        

        #playlist = associated_playlists[0]
        playlist_count = 0

        for playlist in associated_playlists:
            playlist_count+=1
            print "playlist!!! "
            print playlist['name']
            print str(playlist)

            # See if playlist exists as Tuneboss Clientlist
            spotify_url = playlist['external_urls']['spotify']
            try:
                clientlist = Clientlist.objects.get(url=spotify_url)
                last_modified =  clientlist.date_modified
                print 'last_modified' + str(last_modified)
                #lastHourDateTime = date.today() - timedelta(hours = 1)
                last_hour = timezone.now() - datetime.timedelta(hours=1)
                print 'last_hour' + str(last_hour)
                if last_modified > last_hour:
                    client = clientlist.client
                    
                    if clientlist.tracks.count() == 0:
                        all_songs = True
                    else:
                        all_songs = False
                    

                    # Get all tracks
                    owner_id = playlist['owner']['id']
                    sp_playlist_result = sp.user_playlist(owner_id, playlist['id'],
                            fields="tracks,next,followers")
                    # Add followers to clientlist
                    sp_follower_count = sp_playlist_result['followers']['total']
                    clientlist.follower_count = sp_follower_count
                    clientlist.save()

                    # Get the tracks
                    cl_tracks = sp_playlist_result['tracks']['items']

                    # Update and create Artists
                    artist_list = sp_clientlist_artists(cl_tracks, sp)
                    #if en_artist_string is not None:
                    #    en_artists_string += '&id=' + en_artist_string
                    
                    # Update and create albums
                    album_list = sp_clientlist_albums(cl_tracks, sp)

                    # Get clientlist.date_modified to test against songs
                    date_modified = clientlist.date_modified

                    en_tracks_string = ''
                    track_list = []

                    en_artists_string = ''
                    artist_list = []

                    # Count tracks we need to search for
                    track_count = 0
                    #print str(all_songs) + "all_songs"

                    if all_songs == True:
                        # Create all new ClientlistTracks
                        for cl_track in cl_tracks:
                            
                            
                            # Create a clientlist track, tuneboss track, and append to list for update after Echnoest call
                            sp_unique =  cl_track['track']['id']
                            if sp_unique is not None:
                                clientlist_track, en_track_string = add_clientlist_track(cl_track, clientlist)
                                track_count += 1
                                tb_track = clientlist_track.track
                                track_list.append(tb_track)
                                
                                if en_track_string is not None and track_count < 50:
                                    en_tracks_string += '&track_id=' + en_track_string


                    else:
                        # Loop through all tracks returned
                        for cl_track in cl_tracks:

                            # Get date added to see if it needs to be created
                            added_at = parse_date(cl_track['added_at'])
                            if added_at > clientlist.date_modified:
                                
                                track_count += 1

                                # Add clientlist track from track info and get string for EchoNest call
                                clientlist_track, en_track_string = add_clientlist_track(cl_track, clientlist)

                                tb_track = clientlist_track.track
                                track_list.append(tb_track)

                                if en_track_string is not None:
                                    en_tracks_string += '&track_id=' + en_track_string

                    # Get Echonest info for tracks - 10 at a time
                    if track_count > 0 :
                        # Create string of all tracks for request
                        echonest_tracks_url= "http://developer.echonest.com/api/v4/song/profile?api_key=MIFPIXGEUZDLAYXMO&format=json%s&bucket=audio_summary" % en_tracks_string

                        #print 'Time for Echonest, here is the string, ' + echonest_tracks_url

                        # Get echonest info and update track attributes with echonest info
                        get_echonest_tracks_info(echonest_tracks_url, track_list, client)

                    # Update artists and retreive ids
                    artist_list = sp_clientlist_artists(cl_tracks, sp)
                    
                    # Create echonest string for artists
                    for item in artist_list:
                        en_artists_string += '&id=' + str(item)
                        #print en_artists_string

                    # Get Echonest info for artists
                    echonest_artists_url= "http://developer.echonest.com/api/v4/artist/profile?api_key=MIFPIXGEUZDLAYXMO&format=json%s&bucket=discovery&bucket=discovery_rank&bucket=familiarity&bucket=familiarity_rank&bucket=hotttnesss&bucket=hotttnesss_rank&bucket=id:spotify" % en_artists_string



                    #print 'Time for Echonest, here is the string, ' + echonest_artists_url

                    # Get echonest info and update artist attributes with echonest info
                    #get_echonest_artists_info(echonest_artists_url, track_list, client)

                    
                    # Update albums and retreive ids
                    album_list = sp_clientlist_albums(cl_tracks, sp)

            # If it doesn't exist as a Tuneboss clientlist, make it
            except Clientlist.DoesNotExist:
                
                new_clientlist = create_clientlist(client, playlist, current_user, spotify_url, username)
                owner_id = playlist['owner']['id']
                tracks = sp.user_playlist(owner_id, playlist['id'],
                        fields="tracks,next")

                #for track in tracks['tracks']['items']:
                    #print track['track']['name']
                    #print track['track']['artists'][0]['name']
                    
                    #print(json.dumps(track, sort_keys=True, indent=4, separators=(',', ': ')))

                print "Clientlist created for above tracks, run again to add and create songs"
            if playlist_count > 20:
                return
        me = request.user
        return None
    else:
        print "Can't get token for", username

def create_clientlist(client, playlist, current_user, spotify_url, username):

    client_unique = playlist['id']
    print "playlist_client_unique"
    print client_unique
    name = playlist['name']
    client_owner = playlist['owner']['id']
    # Tuneboss
    tuneboss = current_user
    # Playlists
    print "playlists: Not yet"
    # Tracks
    print "tracks: Not yet"
    # URL
    url = spotify_url

    new_clientlist = Clientlist(
        client=client,
        client_unique=client_unique, 
        name=name,
        client_owner=client_owner, 
        tuneboss=current_user,
        url= spotify_url,
        )

    new_clientlist.save()

    new_clientlist_follow = ClientlistFollow(
        user = current_user,
        clientlist=new_clientlist
        )
    new_clientlist_follow.save()

    return new_clientlist

def add_clientlist_track(cl_track, clientlist):
    sp_unique =  cl_track['track']['id']

    try:
        tb_track = Track.objects.get(client_unique=sp_unique)
        new_clientlist_track = create_clientlist_track(cl_track, tb_track, clientlist)
        en_string = None
        return new_clientlist_track, en_string
    except Track.DoesNotExist:
        client = clientlist.client
        sp_track = cl_track['track']
        tb_track = create_track(sp_track, client)
        new_clientlist_track = create_clientlist_track(cl_track, tb_track, clientlist)
        en_string = tb_track.uri
        return new_clientlist_track, en_string

def create_clientlist_track(cl_track, tb_track, clientlist):
    added_at = parse_date(cl_track['added_at']) 
    added_by =  cl_track['added_by']   
    if added_by is None:
        added_by = 'None'
    sp_unique = cl_track['track']['id'] 
    new_clientlist_track = ClientlistTrack(
                                clientlist=clientlist,
                                track=tb_track,
                                added_at=added_at,
                                added_by=added_by,
                                client_unique=sp_unique
                                )
    new_clientlist_track.save()
    return new_clientlist_track

def create_track(sp_track, client, username=None):
    
    client = client
    client_unique = sp_track['id'] 
    name = sp_track['name']
    uri = sp_track['uri'] 
    artist_name = sp_track['artists'][0]['name']
    code=create_code(name, artist_name)
    new_track = Track(
                    client=client,
                    client_unique=client_unique,
                    name=name,
                    uri=uri,
                    artist_name=artist_name,
                    tb_code=code
                    )
    album_id = sp_track['album']['id']
    
    if album_id is not None:
        # Check if album exists
        try:
            album = Album.objects.get(client_unique=album_id)
            new_track.album = album
        except Album.DoesNotExist:
            if username is not None:

                token = util.prompt_for_user_token(username)
                sp = spotipy.Spotify(auth=token)
                sp_album = sp.album(album_id)
                album = create_album(sp_album, client)
                new_track.album = album
    
    new_track.save()
    for artist in sp_track['artists']:
        artist_id = artist['id']
        if artist_id is not None:
            try:
                artist = Artist.objects.get(client_unique=artist_id)
                new_track.artists.add(artist)
            except Artist.DoesNotExist:
                if username is not None:
                    sp_artist = sp.artist(artist_id)
                    artist = create_artist(sp_artist, client)
                    new_track.artists.add(artist)
        
    new_track.save()
    return new_track


def sp_clientlist_artists(cl_tracks, sp):
    client = Client.objects.get(client_name="Spotify")
    artists_list = []
    for cl_track in cl_tracks:
        
        #print(json.dumps(cl_track, sort_keys=True, indent=4, separators=(',', ': ')))
        for sp_artist in cl_track['track']['artists']:

            sp_unique = sp_artist['id']
            if sp_unique is not None:
                artists_list.append(sp_unique)
    
    artists_set = set(artists_list)
    artists_unique = list(artists_set)
    artists_chunks = list(chunks(artists_unique, 20))


    for chunk in artists_chunks:

        sp_artists_result = sp.artists(chunk)
        
        for sp_artist in sp_artists_result['artists']:
            
            sp_unique = sp_artist['id']
            try:
                tb_artist = Artist.objects.get(client_unique=sp_unique)
                tb_artist.popularity = sp_artist['popularity']
                tb_artist.followers = sp_artist['followers']['total']
                tb_artist.save()
            except Artist.DoesNotExist:
                tb_artist = create_artist(sp_artist, client)

    return artists_list


def create_artist(sp_artist, client):
    
    client = client
    #print sp_artist
    sp_unique = sp_artist['id']
    client_unique = sp_unique

    sp_uri = sp_artist['uri']
    uri = sp_uri

    sp_name = sp_artist['name']
    name = sp_name

    sp_href = sp_artist['href']
    href = sp_href

    sp_popularity = sp_artist['popularity']
    popularity = sp_popularity

    sp_followers = sp_artist['followers']['total']
    followers = sp_followers

    if len(sp_artist['images'])==0:
        image_url=None
        image_width=None
        image_height=None
    else:
        for image in sp_artist['images']:
            image_width = image['width']
            image_height = image['width']
            if image_width <= 700 and image_height <= 700:
                image_url = image['url']
                break


    new_artist = Artist(
                    client=client,
                    client_unique=client_unique,
                    uri=uri,
                    name=name,
                    href=href,
                    popularity=popularity,
                    followers=followers,
                    image_url=image_url,
                    image_width=image_width,
                    image_height=image_height
                    )
    new_artist.save()
    return new_artist

def sp_clientlist_albums(cl_tracks, sp):
    client = Client.objects.get(client_name="Spotify")
    albums_list = []

    # Get id for each album in the playlist
    for cl_track in cl_tracks:
        
        #print(json.dumps(cl_track, sort_keys=True, indent=4, separators=(',', ': ')))
        sp_album = cl_track['track']['album']
        
        sp_unique = sp_album['id']
        if sp_unique is not None:
            albums_list.append(sp_unique)
    
    # Break albums list into lists of 20 
    sp_album_lists = list(chunks(albums_list, 20))
    
    # Make all calls together and store 
    results = []
    for albums_list in sp_album_lists:

        sp_albums_result = sp.albums(albums_list)

        results.append(sp_albums_result)
    
    for result in results:
        for sp_album in result['albums']:
            
            sp_unique = sp_album['id']
            try:
                tb_album = Album.objects.get(client_unique=sp_unique)
                tb_album.popularity = sp_album['popularity']
                tb_album.save()
            except Album.DoesNotExist:
                tb_album = create_album(sp_album, client)
    return albums_list


def create_album(sp_album, client):
    #print(json.dumps(sp_album, sort_keys=True, indent=4, separators=(',', ': ')))
    client = client
    sp_unique = sp_album['id']
    client_unique = sp_unique

    sp_uri = sp_album['uri']
    uri = sp_uri

    sp_name = sp_album['name']
    name = sp_name

    sp_href = sp_album['href']
    href = sp_href

    sp_popularity = sp_album['popularity']
    popularity = sp_popularity

    sp_release_date = sp_album['release_date']
    
    sp_release_date_precision = sp_album['release_date_precision']
    
    if sp_release_date_precision == "year":
        strp_string = "%Y"
    elif sp_release_date_precision == "month":
        strp_string = "%Y-%m"
    elif sp_release_date_precision == "day":
        strp_string = "%Y-%m-%d"
    release_date = datetime.datetime.strptime(sp_release_date, strp_string).strftime('%Y-%m-%d')
    

    

    if len(sp_album['images'])==0:
        image_url=None
        image_width=None
        image_height=None
    else:
        for image in sp_album['images']:
            image_width = image['width']
            image_height = image['width']
            if image_width <= 700 and image_height <= 700:
                image_url = image['url']
                break


    new_album = Album(
                    client=client,
                    client_unique=client_unique,
                    uri=uri,
                    name=name,
                    href=href,
                    popularity=popularity,
                    release_date=release_date,
                    image_url=image_url,
                    image_width=image_width,
                    image_height=image_height
                    )
    new_album.save()
    return new_album


def get_echonest_tracks_info(echonest_url, track_list, client):
    print echonest_url

    en_tracks = requests.get(echonest_url).json()

    for en_track in en_tracks['response']['songs']:
        
        print(json.dumps(en_track, sort_keys=True, indent=4, separators=(',', ': ')))
        

        track_name = en_track['title']
        artist_name = en_track['artist_name']
        
        # Create code and match with approriate tb_track in 'track_list'
        code = create_code(track_name, artist_name)

        for track in track_list:
            #print code
            #print track.tb_code
            if track.tb_code == code:
                tb_track = track
        else:
            tb_track = Track.objects.create()

        # Track Features
        track_info = en_track['audio_summary']
        en_unique = en_track['id']
        name = en_track['title']
        tempo = track_info['tempo']
        energy = track_info['energy']
        loudness = track_info['loudness']
        danceability = track_info['danceability']
        speechiness = track_info['speechiness']
        acousticness = track_info['acousticness']
        liveness = track_info['liveness']
        instrumentalness = track_info['instrumentalness']
        key = track_info['key']
        duration = track_info['duration']
        valence = track_info['valence']
        

        tb_track.client=client
        tb_track.en_unique=en_unique
        tb_track.name=name
        #track.popularity=popularity
        tb_track.tempo=tempo
        tb_track.energy=energy
        tb_track.loudness=loudness
        tb_track.danceability=danceability
        tb_track.speechiness=speechiness
        tb_track.acousticness=acousticness
        tb_track.liveness=liveness
        tb_track.instrumentalness=instrumentalness
        tb_track.key=key
        tb_track.duration=duration
        #pictures=pictures
        #album=album
        #artists=artists
        tb_track.save()

        

        

        # Artist Features
        artist_id = en_track['artist_id']
        artist_name = en_track['artist_name']

def get_echonest_artists_info(echonest_url, artist_list, client):
    print echonest_url

    en_artists = requests.get(echonest_url).json()

    print(json.dumps(en_artists, sort_keys=True, indent=4, separators=(',', ': ')))

    for en_artist in en_artists['response']['artists']:
        
        print(json.dumps(en_track, sort_keys=True, indent=4, separators=(',', ': ')))
        
        '''
        track_name = en_track['title']
        artist_name = en_track['artist_name']
        
        # Create code and match with approriate tb_track in 'track_list'
        code = create_code(track_name, artist_name)

        for track in track_list:
            if track.tb_code == code:
                tb_track = track

        # Track Features
        track_info = en_track['audio_summary']
        en_unique = en_track['id']
        name = en_track['title']
        tempo = track_info['tempo']
        energy = track_info['energy']
        loudness = track_info['loudness']
        danceability = track_info['danceability']
        speechiness = track_info['speechiness']
        acousticness = track_info['acousticness']
        liveness = track_info['liveness']
        instrumentalness = track_info['instrumentalness']
        key = track_info['key']
        duration = track_info['duration']
        valence = track_info['valence']
        

        tb_track.client=client
        tb_track.en_unique=en_unique
        tb_track.name=name
        #track.popularity=popularity
        tb_track.tempo=tempo
        tb_track.energy=energy
        tb_track.loudness=loudness
        tb_track.danceability=danceability
        tb_track.speechiness=speechiness
        tb_track.acousticness=acousticness
        tb_track.liveness=liveness
        tb_track.instrumentalness=instrumentalness
        tb_track.key=key
        tb_track.duration=duration
        #pictures=pictures
        #album=album
        #artists=artists
        tb_track.save()

        

        

        # Artist Features
        artist_id = en_track['artist_id']
        artist_name = en_track['artist_name']
        '''


def create_code(name, artist_name):
    sep1 = '['
    sep2 = '-'
    sep3 = '('
    track_name = name.split(sep1, 1)[0].split(sep2, 1)[0].split(sep3, 1)[0].replace(" ", "").lower()
    artist_name = artist_name.split(sep1, 1)[0].split(sep3, 1)[0].replace(" ", "").replace("-", "").lower()

    code = artist_name + track_name

    return code


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

