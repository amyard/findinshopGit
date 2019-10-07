# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item', models.ForeignKey(related_name='history', to='catalog.Item')),
                ('user', models.ForeignKey(related_name='history', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('photo', models.CharField(max_length=255, blank=True)),
                ('phone', models.CharField(max_length=12, blank=True)),
                ('latitude', models.FloatField(null=True, blank=True)),
                ('longitude', models.FloatField(null=True, blank=True)),
                ('country', models.CharField(max_length=75, blank=True)),
                ('city', models.CharField(max_length=75, blank=True)),
                ('user', models.ForeignKey(related_name='social', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uniq', models.CharField(unique=True, max_length=32)),
                ('item', models.ForeignKey(related_name='wishlist', to='catalog.Item')),
                ('user', models.ForeignKey(related_name='wishlist', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
