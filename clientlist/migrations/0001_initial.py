# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('playlist', '__first__'),
        ('music', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('member', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clientlist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('client_unique', models.CharField(max_length=255, null=True, blank=True)),
                ('name', models.CharField(max_length=255, blank=True)),
                ('client_owner', models.CharField(max_length=255, blank=True)),
                ('follower_count', models.IntegerField(null=True, blank=True)),
                ('url', models.CharField(max_length=255, blank=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('client', models.ForeignKey(to='member.Client')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ClientlistFollow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('clientlist', models.ForeignKey(to='clientlist.Clientlist')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ClientlistTrack',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('client_unique', models.CharField(max_length=255, null=True, blank=True)),
                ('added_at', models.DateTimeField()),
                ('added_by', models.CharField(max_length=255, blank=True)),
                ('clientlist', models.ForeignKey(to='clientlist.Clientlist')),
                ('track', models.ForeignKey(to='music.Track')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='clientlist',
            name='members',
            field=models.ManyToManyField(related_name='member_clientlists', through='clientlist.ClientlistFollow', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clientlist',
            name='playlists',
            field=models.ManyToManyField(to='playlist.Playlist'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clientlist',
            name='tracks',
            field=models.ManyToManyField(to='music.Track', through='clientlist.ClientlistTrack'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clientlist',
            name='tuneboss',
            field=models.ForeignKey(related_name='tuneboss_clientlist', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
