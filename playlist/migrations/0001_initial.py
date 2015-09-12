# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('display_name', models.CharField(max_length=255, blank=True)),
                ('picture', models.ImageField(upload_to=b'')),
                ('description', models.CharField(max_length=255, blank=True)),
                ('keyword_variety', models.DecimalField(max_digits=5, decimal_places=2)),
                ('year', models.DecimalField(max_digits=5, decimal_places=2)),
                ('year_variety', models.DecimalField(max_digits=5, decimal_places=2)),
                ('tempo', models.DecimalField(max_digits=5, decimal_places=2)),
                ('tempo_variety', models.DecimalField(max_digits=5, decimal_places=2)),
                ('genre_variety', models.DecimalField(max_digits=5, decimal_places=2)),
                ('hottness', models.DecimalField(max_digits=5, decimal_places=2)),
                ('hottness_variety', models.DecimalField(max_digits=5, decimal_places=2)),
                ('familiarity', models.DecimalField(max_digits=5, decimal_places=2)),
                ('similarity', models.DecimalField(max_digits=5, decimal_places=2)),
                ('artists', models.ManyToManyField(to='music.Artist')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlaylistFollow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('playlist', models.ForeignKey(to='playlist.Playlist')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlaylistTrack',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added_at', models.DateTimeField()),
                ('added_by', models.DateTimeField()),
                ('playlist', models.ForeignKey(to='playlist.Playlist')),
                ('track', models.ForeignKey(to='music.Track')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='playlist',
            name='members',
            field=models.ManyToManyField(related_name='member_playlist', through='playlist.PlaylistFollow', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='playlist',
            name='tracks',
            field=models.ManyToManyField(to='music.Track', through='playlist.PlaylistTrack'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='playlist',
            name='tuneboss',
            field=models.ForeignKey(related_name='tuneboss_playlist', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
