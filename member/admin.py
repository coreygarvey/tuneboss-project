from django.contrib import admin
from django_facebook.admin import FacebookProfileAdmin
from .models import CustomFacebookUser
# Register your models here.

admin.site.register(CustomFacebookUser, FacebookProfileAdmin)