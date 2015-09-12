# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('client_unique', models.CharField(max_length=255, blank=True)),
                ('uri', models.CharField(max_length=255, blank=True)),
                ('name', models.CharField(max_length=255, blank=True)),
                ('href', models.URLField(max_length=255)),
                ('popularity', models.DecimalField(max_digits=5, decimal_places=2)),
                ('release_date', models.DateField()),
                ('image_url', models.URLField(null=True, blank=True)),
                ('image_width', models.IntegerField(null=True, blank=True)),
                ('image_height', models.IntegerField(null=True, blank=True)),
                ('client', models.ForeignKey(to='member.Client')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('client_unique', models.CharField(max_length=255, blank=True)),
                ('en_unique', models.CharField(max_length=255, null=True, blank=True)),
                ('uri', models.CharField(max_length=255, blank=True)),
                ('name', models.CharField(max_length=255, blank=True)),
                ('href', models.URLField(max_length=255)),
                ('popularity', models.IntegerField(null=True, blank=True)),
                ('followers', models.IntegerField(null=True, blank=True)),
                ('hottness', models.DecimalField(null=True, max_digits=5, decimal_places=2, blank=True)),
                ('familiarity', models.DecimalField(null=True, max_digits=5, decimal_places=2, blank=True)),
                ('image_url', models.URLField(null=True, blank=True)),
                ('image_width', models.IntegerField(null=True, blank=True)),
                ('image_height', models.IntegerField(null=True, blank=True)),
                ('albums', models.ManyToManyField(to='music.Album', null=True, blank=True)),
                ('client', models.ForeignKey(to='member.Client')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Term',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('client_unique', models.CharField(max_length=255, null=True, blank=True)),
                ('en_unique', models.CharField(max_length=255, null=True, blank=True)),
                ('uri', models.CharField(max_length=255, blank=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('artist_name', models.CharField(max_length=255, null=True, blank=True)),
                ('tb_code', models.CharField(max_length=255, null=True, blank=True)),
                ('tempo', models.DecimalField(null=True, max_digits=5, decimal_places=2, blank=True)),
                ('energy', models.DecimalField(null=True, max_digits=5, decimal_places=2, blank=True)),
                ('loudness', models.DecimalField(null=True, max_digits=5, decimal_places=2, blank=True)),
                ('danceability', models.DecimalField(null=True, max_digits=5, decimal_places=2, blank=True)),
                ('speechiness', models.DecimalField(null=True, max_digits=5, decimal_places=2, blank=True)),
                ('acousticness', models.DecimalField(null=True, max_digits=5, decimal_places=2, blank=True)),
                ('liveness', models.DecimalField(null=True, max_digits=5, decimal_places=2, blank=True)),
                ('instrumentalness', models.DecimalField(null=True, max_digits=5, decimal_places=2, blank=True)),
                ('key', models.DecimalField(null=True, max_digits=5, decimal_places=2, blank=True)),
                ('duration', models.DecimalField(null=True, max_digits=5, decimal_places=2, blank=True)),
                ('image', models.URLField(null=True, blank=True)),
                ('album', models.ForeignKey(blank=True, to='music.Album', null=True)),
                ('artists', models.ManyToManyField(to='music.Artist', null=True, blank=True)),
                ('client', models.ForeignKey(blank=True, to='member.Client', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
