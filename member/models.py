from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_facebook.models import FacebookModel, get_user_model
from django_facebook.utils import get_profile_model
import logging
import os
logger = logging.getLogger(__name__)


# Clients such as Spotify and Soundcloud
class Client(models.Model):
    client_name = models.CharField(max_length=255, blank=True)

try:
    # There can only be one custom user model defined at the same time
    if getattr(settings, 'AUTH_USER_MODEL', None) == 'member.CustomFacebookUser':
        from django.contrib.auth.models import AbstractUser, UserManager
        class CustomFacebookUser(AbstractUser, FacebookModel):
            '''
            The django 1.5 approach to adding the facebook related fields
            '''
            objects = UserManager()
            # add any customizations you like
            clients = models.ManyToManyField(Client, through='ClientProfile')
            
except ImportError as e:
    logger.info('Couldnt setup FacebookUser, got error %s', e)
    pass


# User profiles for clients like Spotify and Soundcloud
class ClientProfile(models.Model):
    user = models.ForeignKey(CustomFacebookUser, related_name="clientProfiles")
    client = models.ForeignKey(Client, blank=True, null=True)
    username = models.CharField(max_length=255, blank=True)