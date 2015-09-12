from django.conf import settings
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.template.context import RequestContext
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import View
from django_facebook import exceptions as facebook_exceptions, \
    settings as facebook_settings
from django_facebook.connect import CONNECT_ACTIONS, connect_user
from django_facebook.decorators import facebook_required_lazy
from django_facebook.utils import next_redirect, get_registration_backend, \
    to_bool, error_next_redirect, get_instance_for
from open_facebook import exceptions as open_facebook_exceptions
from open_facebook.utils import send_warning
from open_facebook import OpenFacebook

from utils import get_echonest, update_user_playlists, create_track

from .forms import ClientUsernameForm

from member.models import Client, ClientProfile
from clientlist.models import Clientlist
from music.models import Track

import re
import logging
import json

import spotipy.util as util
import spotipy


def home(request):
  context = RequestContext(request)
  return render_to_response('home.html', context)

def bootstrap(request):
  context = RequestContext(request)
  return render_to_response('bootstrap.html', context)  

def spotify(request):
  #playlists = get_user_playlists('123770737', request)
  #print playlists
  context = RequestContext(request)
  #context['playlists'] = playlists
  return render_to_response('home.html', context)

def echonest(request):
  response = get_echonest()
  print response
  context = RequestContext(request)
  return render_to_response('home.html', context)

def get_spotify_username(request):
    me = request.user
    context = {}
    if me.id is not None:
      access_token = me.access_token
      print access_token
      graph = OpenFacebook(access_token)
      if access_token is not None:
        listen_data = graph.get('me/music.listens')
        user_listens = []
        listens = listen_data['data']
        for listen in listens:
          tmp = []
          song_name = listen['data']['song']['title']
          client_url = listen['data']['song']['url']
          client_unique = re.search('track\/(.*)', client_url).group(1)
          tmp.append(song_name)
          tmp.append(client_unique)
          user_listens.append(tmp)

          print(json.dumps(song_name, sort_keys=True, indent=4, separators=(',', ': ')))
        context['user_listens'] = user_listens


    current_user = request.user
    print 'something'
    if current_user.id is not None:
      
      clientProfiles = current_user.clients.all()
      if clientProfiles:
        print clientProfiles
      else:
        print "clientProfiles"

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ClientUsernameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            
            # Get information from username form
            username = form.cleaned_data["username"]
            client_name = form.cleaned_data["client"]

            # Client object and ID based on client chosen by user
            client = Client.objects.get(client_name=client_name)
            client_id = client.id

            # Check if the user has this a profile for this client, if not create it.
            try:
              client = current_user.clients.get(id=client_id)
              
            except client.DoesNotExist:
              new_client_profile = ClientProfile(user=current_user, client=client, username=username)
              new_client_profile.save()


            # Get user's playlists - Inside this helper function we will decide whether the data needs to be added to TuneBoss, updated or is already present.
            playlists = update_user_playlists(client, username, request)
            
            context = {}
            if current_user.id is not None:
              context['user_clientlists'] = current_user.member_clientlists.all()
            return render(request, 'home.html', context)

    # if a GET (or any other method) we'll create a blank form
    else: 
        form = ClientUsernameForm()

    
    
    if current_user.id is not None:
      print "current_user " + str(current_user.email)
      context['user_clientlists'] = current_user.member_clientlists.all()
    context['form'] = form
    return render(request, 'home.html', context)

def clientlist(request, clientlist_id=None):
  current_user = request.user
  access_token = current_user.access_token

  client_username = current_user.clientProfiles.get(user=current_user).username
  user_listens = userListens(access_token, client_username)
  chosen_clientlist = Clientlist.objects.get(id=clientlist_id)
  print chosen_clientlist
  context = {}
  if current_user.id is not None:
      context['user_listens'] = user_listens
      context['user_clientlists'] = current_user.member_clientlists.all()
      context['clientlist'] = chosen_clientlist
  return render(request, 'clientlist.html', context)


def userListens(access_token, client_username):
  # Form has username info to get access_token from Spotify
  username = client_username
  token = util.prompt_for_user_token(username)

  sp = spotipy.Spotify(auth=token)
  graph = OpenFacebook(access_token)
  if access_token is not None:
    listen_data = graph.get('me/music.listens')
    user_listens = []
    listens = listen_data['data']
    for listen in listens:
      tmp = []
      song_name = listen['data']['song']['title']
      client_url = listen['data']['song']['url']
      client_unique = re.search('track\/(.*)', client_url).group(1)
      print client_unique
      
      # Get tuneboss track if it exists, othewise create it.
      try:
        tb_track = Track.objects.get(client_unique=client_unique)
      except Track.DoesNotExist:
        sp_track = sp.track(client_unique)
        client = Client.objects.get(client_name='Spotify')
        tb_track = create_track(sp_track, client, username)



      artist_name = tb_track.artist_name
      
      tmp.append(client_unique)
      tmp.append(song_name)
      tmp.append(artist_name)
      if listen['data'].get('playlist'):
        playlist = listen['data']['playlist']['title']
        tmp.append(playlist)
      user_listens.append(tmp)

      print(json.dumps(song_name, sort_keys=True, indent=4, separators=(',', ': ')))
  return user_listens

class HomeView(View):
    

    # if this is a POST request we need to process the form data
    #if request.method == 'POST':
    def post(self, request):
      # create a form instance and populate it with data from the request:
      form = ClientUsernameForm(request.POST)
      # check whether it's valid:
      if form.is_valid():
          # process the data in form.cleaned_data as required
          # ...
          # redirect to a new URL:
          
          # Get information from username form
          username = form.cleaned_data["username"]
          client_name = form.cleaned_data["client"]

          # Client object and ID based on client chosen by user
          client = Client.objects.get(client_name=client_name)
          client_id = client.id

          # Check if the user has this a profile for this client, if not create it.
          try:
            client = current_user.clients.get(id=client_id)
            
          except client.DoesNotExist:
            new_client_profile = ClientProfile(user=current_user, client=client, username=username)
            new_client_profile.save()


          # Get user's playlists - Inside this helper function we will decide whether the data needs to be added to TuneBoss, updated or is already present.
          playlists = update_user_playlists(client, username, request)
          
          
          return HttpResponseRedirect('/home_view/')

    # if a GET (or any other method) we'll create a blank form
    def get(self, request):
      current_user = request.user
      form = ClientUsernameForm()

    
      context = {}
      context['user_clientlists'] = current_user.member_clientlists.all()
      context['form'] = form
      return render(request, 'spotify_username.html', context)
